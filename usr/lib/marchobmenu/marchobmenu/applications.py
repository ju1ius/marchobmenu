import os, re
import xdg.DesktopEntry, xdg.Menu
#from xdg.Exceptions import *
import base

class ApplicationsMenu(base.Menu):

    def __init__(self):
        super(ApplicationsMenu, self).__init__()
        xdg.Config.setWindowManager('openbox')
        self.filter_debian = os.path.isfile('/usr/bin/update-menus')

    def parse_config(self):
        super(ApplicationsMenu, self).parse_config()
        self.terminal_emulator = self.config.get('Menu', 'terminal')

    def parse_menu_file(self, menu_file):
        menu = xdg.Menu.parse(menu_file)
        output = self.menu_entry(menu)
        output = self.format_menu(output)
        return output
    
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
        cmd = self.exe_regex.sub('', de.getExec())
        if de.getTerminal():
            cmd = self.terminal_emulator % {"title": name, "command": cmd}
        # Get icon
        icon = self.find_icon(de.getIcon().encode('utf-8')) if self.show_icons else ''

        indent = "  " * level
        return self.format_application(name, cmd, icon, indent)

