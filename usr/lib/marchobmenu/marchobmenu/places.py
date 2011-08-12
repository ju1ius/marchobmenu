import os
import base

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


class PlacesMenu(base.Menu):

    def parse_config(self):
        super(PlacesMenu, self).parse_config()
        self.file_manager = self.config.get("Menu", "filemanager")
        self.show_files = self.config.getboolean("Places", "show_files")
        if self.show_icons:
            self.folder_icon = self.config.get("Icons", "folders")
            self.file_icon = self.config.get("Icons", "files")
    
    def parse_path(self, path):
        folder_icon = self.find_icon(self.folder_icon) if self.show_icons else '""'
        file_icon = self.find_icon(self.file_icon) if self.show_icons else '""'
        fm = self.file_manager
        output = [
            self.format_application(
                'Browse Here...', '%s "%s"' % (fm, path),
                folder_icon, '  '
            ),
            self.format_separator('  ')
        ]
        append = output.append
        files = sorted_listdir(path, self.show_files)
        for filename in files:
            filepath = os.path.join(path, filename)
            if filename.startswith('.') or filename.endswith('~'):
                continue
            if os.path.isfile(filepath):
                cmd = "%s %s" % (fm, filepath)
                item = self.format_application(filename, cmd, file_icon, '  ')
            else:
                cmd = 'mom-places "%s"' % filepath
                item = self.format_exec_menu(filepath, filename, cmd, folder_icon, '  ')
            append(item)
        return self.format_menu( "".join(output) )


if __name__ == "__main__":
    path = os.path.abspath(os.path.expanduser(sys.argv[1]))
    menu = PlacesMenu()
    print menu.parse_path(path)


