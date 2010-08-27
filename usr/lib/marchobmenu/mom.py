#!/usr/bin/python
# coding=utf-8

import os, sys, re, time

import xdg.Config, xdg.BaseDirectory, xdg.DesktopEntry, xdg.Menu
from xdg.Exceptions import *

from xml.sax.saxutils import escape, quoteattr


def print_menu(menu):

  for entry in menu.getEntries():

    if isinstance(entry, xdg.Menu.Separator):
      print '<separator/>'

    elif isinstance(entry, xdg.Menu.Menu):
      print '<menu id=%s label=%s>' % (
        quoteattr(entry.Name.encode('utf-8')),
        quoteattr(entry.getName().encode('utf-8'))
      )
      print_menu(entry)
      print '</menu>'

    elif isinstance(entry, xdg.Menu.MenuEntry):
      print '  <item label=%s>' % quoteattr(entry.DesktopEntry.getName().encode('utf-8'))
      cmd = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', entry.DesktopEntry.getExec())
      if entry.DesktopEntry.getTerminal():
        cmd = 'x-terminal-emulator -title "%s" -e %s' % (
          entry.DesktopEntry.getName().encode('utf-8'),
          cmd
        )
      print '    <action name="Execute"><command>%s</command></action>' % escape(cmd)
      print '  </item>'



filename = 'mom-applications.menu'
if len(sys.argv) > 1:
  filename = sys.argv[1]
  if not filename.endswith('.menu'): filename += '.menu'

xdg.Config.setWindowManager('openbox')
menu = xdg.Menu.parse(filename)

print '<?xml version="1.0" encoding="UTF-8"?>'
print '<openbox_pipe_menu>'
print_menu(menu)
print '</openbox_pipe_menu>'

