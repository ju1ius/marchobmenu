#!/usr/bin/python
# coding=utf-8

import os, sys
import marchobmenu.recently_used

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'clear':
            with open(os.path.expanduser('~/.recently-used.xbel'), 'w') as f:
                f.write("""<?xml version="1.0" encoding="UTF-8"?>
<xbel version="1.0"
      xmlns:bookmark="http://www.freedesktop.org/standards/desktop-bookmarks"
      xmlns:mime="http://www.freedesktop.org/standards/shared-mime-info"
>
</xbel>""")
    else:
        menu = marchobmenu.recently_used.RecentlyUsedMenu()
        print menu.parse_bookmarks()
