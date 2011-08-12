import os, sys, stat, re, StringIO, sqlite3, ConfigParser
from xml.sax.saxutils import escape, quoteattr
import xdg.IconTheme

class Menu(object):

    default_config = """
[Menu]
filemanager: thunar
terminal: x-terminal-emulator -T '%(title)s' -e '%(command)s'
[Places]
show_files: yes
[Recently Used]
max_items: 20
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
        cache_dir = os.path.expanduser('~/.cache/marchobmenu')
        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir)
        self.parse_config()
        self.exe_regex = re.compile(r' [^ ]*%[fFuUdDnNickvm]')
        if self.show_icons:
            self.open_cache()

    def __del__(self):
        if self.show_icons:
            self.close_cache

    def parse_config(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(StringIO.StringIO(self.default_config))
        self.config.read([
            '/etc/marchobmenu/menu.conf',
            os.path.expanduser('~/.config/marchobmenu/menu.conf')
        ])

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
    
    def format_menu(self, content):
      return """<?xml version="1.0" encoding="UTF-8"?>
<openbox_pipe_menu>\n%s</openbox_pipe_menu>""" % content

    def format_text_item(self, txt):
        return "<item label=%s />\n" % quoteattr(txt)

    def format_separator(self, indent=''):
        return "%s<separator/>\n" % indent

    def format_application(self, name, cmd, icon, indent=''):
        return """%(i)s<item label=%(n)s icon=%(icn)s>
%(i)s  <action name='Execute'>
%(i)s    <command>%(c)s</command>
%(i)s  </action>
%(i)s</item>
""" % {
            "i": indent, "n": quoteattr(name), "icn": quoteattr(icon),
            "c": escape(cmd)
        }

    def format_submenu(self, id, name, icon, submenu, indent=''):
        return """%(i)s<menu id=%(id)s label=%(n)s icon=%(icn)s>
  %(sub)s%(i)s</menu>
""" % {
            "i": indent, "id": quoteattr(id), "n": quoteattr(name),
            "icn": quoteattr(icon), "sub": submenu
        }

    def format_exec_menu(self, id, label, cmd, icon, indent=''):
        return "%(i)s<menu id=%(id)s label=%(n)s execute=%(cmd)s icon=%(icn)s/>\n" % {
            "i": indent, "id": quoteattr(id), "n": quoteattr(label),
            "cmd": quoteattr(cmd), "icn": quoteattr(icon)
        }

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
