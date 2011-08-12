#!/usr/bin/python
# coding=utf-8

import os, sys
import marchobmenu.bookmarks

if __name__ == "__main__":
    menu = marchobmenu.bookmarks.BookmarksMenu()
    print menu.parse_bookmarks()
