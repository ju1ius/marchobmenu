#!/usr/bin/python
# coding=utf-8

import os, sys
from xml.sax.saxutils import escape, quoteattr
import marchobmenu

def sort_ci(inlist, minisort=True):
  """
  Case insensitive sorting)
  If minisort=False, sort_ci will not sort sets of entries
  for which entry1.lower() == entry2.lower()
  i.e. sort_ci(['fish', 'FISH', 'fIsh'], False)
  returns ['fish', 'FISH', 'fIsh']
  instead of ['FISH', 'fIsh', 'fish']
  """
  sortlist = []
  newlist = []
  sortdict = {}
  for entry in inlist:
    try:
      lentry = entry.lower()
    except AttributeError:
      sortlist.append(lentry)
    else:
      try:
        sortdict[lentry].append(entry)
      except KeyError:
        sortdict[lentry] = [entry]
        sortlist.append(lentry)

  sortlist.sort()
  for entry in sortlist:
    try:
      thislist = sortdict[entry]
      if minisort: thislist.sort()
      newlist = newlist + thislist
    except KeyError:
      newlist.append(entry)
  return newlist


def sorted_listdir(path, show_files=True):
  """
  Returns the content of a directory by showing directories first
  and then files by ordering the names alphabetically
  """
  items = os.listdir(path)
  files = sort_ci(d for d in items if os.path.isdir(os.path.join(path, d)))
  if show_files:
    files.extend(sort_ci(f for f in items if os.path.isfile(os.path.join(path, f))))
  return files


class PlacesMenu(marchobmenu.ApplicationsMenu):

    def parse_config(self):
        super(PlacesMenu, self).parse_config()
        self.file_manager = self.config.get("Menu", "filemanager")
        self.show_files = self.config.getboolean("Places", "show_files")
        self.folder_icon = self.config.get("Icons", "folders")
        self.file_icon = self.config.get("Icons", "files")
    
    def parse_path(self, path):
        if self.show_icons:
            self.open_cache()
            folder_icon = quoteattr( self.find_icon(self.folder_icon) )
            file_icon = quoteattr( self.find_icon(self.file_icon) )
            self.close_cache()
        else:
            folder_icon = ''
            file_icon = ''
        fm = self.file_manager
        output = []
        append = output.append
        append(
"""<?xml version="1.0" encoding="UTF-8"?>
<openbox_pipe_menu>
  <item label="Browse Here.." icon=%s >
    <action name="Execute">
      <execute>%s "%s"</execute>
    </action>
  </item>
  <separator />""" % (folder_icon, escape(fm), escape(path))
        )
        files = sorted_listdir(path, self.show_files)
        for filename in files:
            filepath = os.path.join(path, filename)
            if filename.startswith('.') or filename.endswith('~'):
                continue
            if os.path.isfile(filepath):
                item = """  <item label=%s icon=%s>
    <action name="Execute">
      <execute>%s %s</execute>)
    </action>"
  </item>""" % (quoteattr(filename), file_icon, fm, escape(filepath))
            else:
                item = "  <menu id=%s label=%s icon=%s execute=%s />" % (
                    quoteattr(filepath), quoteattr(filename), folder_icon,
                    quoteattr( "%s '%s'" % (sys.argv[0], escape(filepath)) )
                )
            append(item)
        append('</openbox_pipe_menu>')
        return "\n".join(output)



if __name__ == "__main__":
    path = os.path.abspath(os.path.expanduser(sys.argv[1]))
    menu = PlacesMenu()
    print menu.parse_path(path)
