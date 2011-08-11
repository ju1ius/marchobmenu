#!/usr/bin/python
# coding=utf-8

import os, sys, urllib
from xml.sax.saxutils import escape, quoteattr
import marchobmenu


###########################################################
# The bookmarks menu class
#
class BookmarksMenu(marchobmenu.ApplicationsMenu):

    def parse_config(self):
        super(BookmarksMenu, self).parse_config()
        self.file_manager = self.config.get("Menu", "filemanager")
        self.bookmark_icon = self.config.get("Icons", "bookmarks")

    def parse_bookmarks(self):
        if self.show_icons:
            self.open_cache()
            icon = quoteattr( self.find_icon(self.bookmark_icon) )
            self.close_cache()
        else:
            icon = ''
        bookmarks = [ ('~', 'Home') ]
        append = bookmarks.append
        with open(os.path.expanduser('~/.gtk-bookmarks')) as f:
            for line in f:
                path, label = line.strip().partition(' ')[::2]
                if not label:
                    label = os.path.basename(os.path.normpath(path))
                append((path, label))
        output = ['<?xml version="1.0" encoding="UTF-8"?>','<openbox_pipe_menu>']
        append = output.append
        fm = self.file_manager
        for path, label in bookmarks:
            label = quoteattr( urllib.unquote(label) )
            path = escape(path)
            append("""  <item label=%s icon=%s >
    <action name="Execute">
      <execute>%s "%s"</execute>
    </action>
  </item>""" % ( label, icon, fm, path )
            )
        append('</openbox_pipe_menu>')
        return "\n".join(output)

if __name__ == "__main__":
    menu = BookmarksMenu()
    print menu.parse_bookmarks()
