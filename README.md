Marchobmenu is an adaptation for Openbox of Marchfluxmenu and mint-fm2.
http://code.google.com/p/marchfluxmenu

Marchobmenu monitors for newly installed/removed applications, and maintains a pipemenu, listing and categorizing them like the Gnome/Xfce/Lxde menu.
It does so by reading the .desktop entries in /usr/share/applications and converting them to a xml file located in ~/.config/openbox/marchobmenu/applications.xml

Marchobmenu is written in pure bash and only requires the inotify-tools package.

There is also a "Places" menu available that will allow you to browse your filesystem from your Openbox menu.
Again it is a port in bash of the "Places" script from Crunchbang Linux.

See the INSTALL file for installing instructions.