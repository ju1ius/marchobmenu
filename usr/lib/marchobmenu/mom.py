#!/usr/bin/python
# coding=utf-8

import os, sys, re, ConfigParser, StringIO

import xdg.Config, xdg.BaseDirectory, xdg.DesktopEntry, xdg.Menu, xdg.Exceptions

from xml.sax.saxutils import escape, quoteattr


################################################################################
#		FUNCTIONS
#-------------------------------------------------------------------------------
def print_separator(entry):
  print '<separator/>'

def print_submenu(entry):
  print '<menu id=%s label=%s>' % (
    quoteattr(entry.Name.encode('utf-8')),
    quoteattr(entry.getName().encode('utf-8'))
  )
  print_menu(entry)
  print '</menu>'

def print_exec(entry):
  # Skip Debian specific menu entries
  if filter_debian and entry.DesktopEntry.get('Categories', list=False).startswith('X-Debian'):
    return
  print '  <item label=%s>' % quoteattr(entry.DesktopEntry.getName().encode('utf-8'))
  cmd = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', entry.DesktopEntry.getExec())
  if entry.DesktopEntry.getTerminal():
    cmd = 'x-terminal-emulator -e %s' % (cmd)
  print '    <action name="Execute"><command>%s</command></action>' % escape(cmd)
  print '  </item>'

def print_menu(menu):
  for entry in menu.getEntries():
    if isinstance(entry, xdg.Menu.Separator):
      print_separator(entry)
    elif isinstance(entry, xdg.Menu.Menu):
      print_submenu(entry)
    elif isinstance(entry, xdg.Menu.MenuEntry):
      print_exec(entry)
#-------------------------------------------------------------------------------
#		/FUNCTIONS
################################################################################



################################################################################
#		MAIN
#-------------------------------------------------------------------------------
if __name__ == "__main__":

  filter_debian = os.path.isfile('/usr/bin/update-menus')

  xdg.Config.setWindowManager('openbox')
  menu = xdg.Menu.parse('mom-applications.menu')

  print '<?xml version="1.0" encoding="UTF-8"?>'
  print '<openbox_pipe_menu>'
  print_menu(menu)
  print '</openbox_pipe_menu>'
#-------------------------------------------------------------------------------
#		/MAIN
################################################################################

