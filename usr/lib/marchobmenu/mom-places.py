#!/usr/bin/python
# coding=utf-8

import os, sys
import marchobmenu.places

if __name__ == "__main__":
    menu = marchobmenu.places.PlacesMenu()
    try:
        path = os.path.abspath(os.path.expanduser(sys.argv[1]))
        print menu.parse_path(path)
    except Exception, why:
        print menu.format_menu(menu.format_text_item(
            "Error: %s" % why    
        ))
