Marchobmenu is an automated XDG Menu system for Openbox.

Marchobmenu monitors for newly installed/removed applications,
and maintains a pipemenu, listing and categorizing them like the Gnome/Xfce/Lxde menu.

It aims to be fast and lightweight:
  * regeneration of the menu takes less than half a second when icons are cached
  * the daemon hardly consumes more than 150 Kb of RAM
  * on Debian/dpkg based systems, it can make use of the dpkg-triggers system,
    in order to consume even less resources.

Also available are two pipemenus:
  * mom-bookmarks: browse the filesystem from your Openbox menu
  * mom-places: list GTK Bookmarks in your Openbox menu

For help, please [Check the wiki] (http://github.com/ju1ius/marchobmenu/wiki)

-----------------------------------------------------------------------
Marchobmenu is inspired by:
  * [xdg-menu] (http://cvs.fedoraproject.org/viewvc/devel/openbox/xdg-menu)
  * [mint-fm2] (http://packages.linuxmint.com/pool/main/m/mint-fm2/)

The "Places" script is a python port of
Kacper Wysocki's obpipemenu-places for [Crunchbang Linux](http://www.crunchbanglinux.org)

