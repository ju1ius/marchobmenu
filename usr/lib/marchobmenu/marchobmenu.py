import os, sys, stat, re, StringIO, sqlite3, ConfigParser
from xml.sax.saxutils import escape, quoteattr
import xdg.Config, xdg.BaseDirectory, xdg.DesktopEntry, xdg.Menu, xdg.IconTheme
#from xdg.Exceptions import *

class ApplicationsMenu(object):

    default_config = """
[Menu]
filemanager: thunar
terminal: x-terminal-emulator -T '%(title)s' -e '%(command)s'
[Places]
show_files: yes
[Icons]
show: yes
use_gtk_theme: yes
theme: Mint-X
size: 24
default: application-x-executable
bookmarks: user-bookmarks
folders: folder
files: gtk-file
"""

    def __init__(self):
        xdg.Config.setWindowManager('openbox')
        cache_dir = os.path.expanduser('~/.cache/marchobmenu')
        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir)
        self.filter_debian = os.path.isfile('/usr/bin/update-menus')
        self.parse_config()

    def parse_config(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(StringIO.StringIO(self.default_config))
        self.config.read([
            '/etc/marchobmenu/menu.conf',
            os.path.expanduser('~/.config/marchobmenu/menu.conf')
        ])

        self.terminal_emulator = self.config.get('Menu', 'terminal')

        self.show_icons = self.config.getboolean('Icons', 'show')
        if self.show_icons:
            self.default_icon = self.config.get('Icons', 'default')
            self.icon_size = self.config.getint('Icons', 'size')
            self.use_gtk_theme = self.config.getboolean('Icons', 'use_gtk_theme')
            if self.use_gtk_theme:
                try:
                    import pygtk
                    pygtk.require('2.0')
                    import gtk
                    gtk_settings = gtk.settings_get_default()
                    self.theme = gtk_settings.get_property('gtk-icon-theme-name')
                except:
                    self.use_gtk_theme = False
                    self.theme = self.config.get('Icons','theme')
            else:
                self.theme = self.config.get('Icons','theme')

    def parse_menu_file(self, menu_file):
        if self.show_icons:
            self.open_cache()
        menu = xdg.Menu.parse(menu_file)
        output = self.menu_entry(menu)
        output = self.format_menu(output)
        if self.show_icons:
            self.close_cache()
        return output

    def open_cache(self):
        db_file = os.path.expanduser('~/.cache/marchobmenu/icons.db')
        if not os.path.isfile(db_file):
            os.mknod(db_file, 0644|stat.S_IFREG)
        self.cache_conn = sqlite3.connect(db_file)
        self.cache_conn.execute(
            "CREATE TABLE IF NOT EXISTS cache(key TEXT, path TEXT)"
        )
        self.cache_conn.row_factory = sqlite3.Row
        self.cache_cursor = self.cache_conn.cursor()

    def close_cache(self):
        self.cache_conn.commit()
        self.cache_cursor.close()
    
    def menu_entry(self, menu, level=0):
        output = []
        append = output.append
        for entry in menu.getEntries():
            if isinstance(entry, xdg.Menu.Separator):
                append( self.separator(entry, level) )
            elif isinstance(entry, xdg.Menu.Menu):
                append( self.submenu(entry, level) )
            elif isinstance(entry, xdg.Menu.MenuEntry):
                append( self.application(entry, level) )
        return "".join(output)

    def format_menu(self, content):
      return """<?xml version="1.0" encoding="UTF-8"?>
<openbox_pipe_menu>

  %s
</openbox_pipe_menu>""" % content

    def format_separator(self, indent):
        return "%s<separator/>\n" % indent

    def format_application(self, name, cmd, icon, indent):
        return """%(i)s<item label=%(n)s icon=%(icn)s>
    %(i)s  <action name='Execute'>
    %(i)s    <command>%(c)s</command>
    %(i)s  </action>
    %(i)s</item>
    """ % {
            "i": indent, "n": quoteattr(name), "icn": quoteattr(icon),
            "c": escape(cmd)
        }

    def format_submenu(self, id, name, icon, submenu, indent):
        return """%(i)s<menu id=%(id)s label=%(n)s icon=%(icn)s>
    %(sub)s%(i)s</menu>
    """ % {
            "i": indent, "id": quoteattr(id), "n": quoteattr(name),
            "icn": quoteattr(icon), "sub": submenu
        }

    def separator(self, entry, level):
        indent = "  " * level
        return self.format_separator(indent)

    def submenu(self, entry, level):
        id = entry.Name.encode('utf-8')
        name = entry.getName().encode('utf-8')
        icon = self.find_icon(entry.getIcon().encode('utf-8')) if self.show_icons else ''
        submenu = self.menu_entry(entry, level+1)
        indent = "  " * level
        return self.format_submenu(id, name, icon, submenu, indent)

    def application(self, entry, level):
        de = entry.DesktopEntry
        # Skip Debian specific menu entries
        if self.filter_debian and de.get('Categories', list=False).startswith('X-Debian'):
            return
        # Escape entry name
        name = de.getName().encode('utf-8')
        # Strip command arguments
        cmd = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', de.getExec())
        if de.getTerminal():
            cmd = self.terminal_emulator % {"title": name, "command": cmd}
        # Get icon
        icon = self.find_icon(de.getIcon().encode('utf-8')) if self.show_icons else ''

        indent = "  " * level
        return self.format_application(name, cmd, icon, indent)

  
    def find_icon(self, name):
        """Finds and cache icons"""
        if not name:
            name = self.default_icon
        if os.path.isabs(name):
            key = name
        else:
            key = name + '::' + self.theme      
        cached = self.fetch_cache_key(key)
        if cached:
            return cached['path'].encode('utf-8')
        else:
            path = self.get_icon_path(name)
            if path:
                self.add_cache_key(key, path)
                return path.encode('utf-8')
        return ''

    def get_icon_path(self, name):
        # Openbox doesn't support svg in menu
        path = xdg.IconTheme.getIconPath(
            name, self.icon_size, self.theme, ['png','xpm']
        )
        if not path or path.endswith('.svg'):
            path = xdg.IconTheme.getIconPath(
                self.default_icon, self.icon_size, self.theme, ['png', 'xpm']
            )
        return path

    def fetch_cache_key(self, key):
        self.cache_cursor.execute(
            'SELECT cache.key, cache.path FROM cache WHERE cache.key = ?',
            [key]
        )
        return self.cache_cursor.fetchone()

    def add_cache_key(self, key, path):
        self.cache_cursor.execute(
            'INSERT INTO cache(key, path) VALUES(?,?)',
            [key, path]
        )
