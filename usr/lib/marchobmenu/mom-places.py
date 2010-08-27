#!/usr/bin/python
# coding=utf-8

import os, sys, platform
from xml.sax.saxutils import escape, quoteattr


def sort_ci(inlist, minisort=True):
  """
  Case insensitive sorting
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


def sorted_listdir(path):
  """
  Returns the content of a directory by showing directories first
  and then files by ordering the names alphabetically
  """
  items = os.listdir(path)
  files = sort_ci([ d for d in items if os.path.isdir(os.path.join(path, d)) ])
  files.extend(sort_ci([ f for f in items if os.path.isfile(os.path.join(path, f)) ]))
  return files



script_path = __file__

if platform.system() == 'Windows':
  open_cmd = "start"
elif platform.system() == 'Darwin':
  open_cmd = "open"
else:
  # assume Linux
  open_cmd = "xdg-open"

path = os.path.abspath(os.path.expanduser(sys.argv[1]))
file_manager = sys.argv[2]

#files = os.listdir(path)
#files.sort()

files = sorted_listdir(path)

print '<openbox_pipe_menu>'

# "Browse here..." lauches this dir
print """<item label="Browse Here..">
  <action name="Execute">
    <execute>%s "%s"</execute>
  </action>
</item>
<separator />""" % (
  escape(file_manager),
  escape(path)
)


for filename in files:
  filepath = os.path.join(path, filename)

  if filename.startswith('.') or filename.endswith('~'): continue

  if os.path.isfile(filepath):
    print """<item label=%s>
  <action name="Execute">
    <execute>%s %s</execute>
  </action>"
</item>""" % (
      quoteattr(filename),
      open_cmd,
      escape(filepath)
    )
  else:
    print "<menu id=%s label=%s execute=%s />" % (
      quoteattr(filepath),
      quoteattr(filename),
      quoteattr(
        script_path + " "
        + filepath.replace(' ', '\ ') + " "
        + file_manager
      )
    )


print '</openbox_pipe_menu>'

