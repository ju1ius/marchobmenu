import os, sys, re, urllib
from xml.etree import cElementTree as ElementTree
import base


class RecentlyUsedMenu(base.Menu):

    def __init__(self):
        super(RecentlyUsedMenu, self).__init__()
        self.exe_regex = re.compile(r"'(.*) %[a-zA-Z]'")
        mime_ns = 'http://www.freedesktop.org/standards/shared-mime-info'
        bookmark_ns = 'http://www.freedesktop.org/standards/desktop-bookmarks' 
        self.find_mime = 'info/metadata/{%s}mime-type' % mime_ns
        self.find_bookmark = 'info/metadata/{%(ns)s}applications/{%(ns)s}application' % { "ns": bookmark_ns }

    def parse_config(self):
        super(RecentlyUsedMenu, self).parse_config()
        self.max_items = self.config.getint("Recently Used", "max_items")
        if self.show_icons:
            self.folder_icon = self.config.get("Icons", "folders")
            self.file_icon = self.config.get("Icons", "files")

    def parse_bookmarks(self):
        self.folder_icon = self.find_icon(self.folder_icon) if self.show_icons else '""'
        self.file_icon = self.find_icon(self.file_icon) if self.show_icons else '""'
        source = os.path.expanduser("~/.recently-used.xbel")
        tree = ElementTree.parse(source)
        last_index = - (self.max_items -1)
        bookmarks = tree.findall('/bookmark')[last_index:-1]
        bookmarks.reverse()
        output = map(self.parse_item, bookmarks)
        output.extend([
            self.format_separator('  '),
            self.format_application('Clear', 'mom-recently-used clear', '', '  ')
        ])
        return self.format_menu( "".join(output) )

    def parse_item(self, el):
        href = el.get('href')
        label = urllib.unquote( href.rsplit('/',1)[1] )
        mime_type = el.find(self.find_mime).get('type')
        cmd = el.find(self.find_bookmark).get('exec')
        cmd = self.exe_regex.sub(r'\1', cmd)
        cmd = '%s "%s"' % (cmd, href)
        if self.show_icons:
            icon = self.folder_icon if mime_type == "inode/directory" else self.file_icon
        else:
            icon = ''
        return self.format_application(label, cmd, icon, '  ')

