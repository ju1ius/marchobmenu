package="marchobmenu"
version="3.1"

export prefix=/usr/local
export sysconfdir=/etc

CC=gcc
CFLAGS=-W -Wall -pedantic
LDFLAGS=-linotifytools
EXEC=usr/bin/marchobmenud
SRC=src/marchobmenud.c

marchobmenud:
	mkdir -p usr/bin
	${CC} ${SRC} -o ${EXEC} ${LDFLAGS} ${CFLAGS}

.PHONY: clean install uninstall

clean:
	rm ${EXEC}

install:
	install -d ${prefix}/lib/marchobmenu/marchobmenu
	install -m 0755 usr/lib/marchobmenu/marchobmenu/*.py ${prefix}/lib/marchobmenu/marchobmenu
	install -m 0755 usr/lib/marchobmenu/*.py ${prefix}/lib/marchobmenu
	install -d ${prefix}/share/desktop-directories
	install -m 0755 usr/share/desktop-directories/* ${prefix}/share/desktop-directories
	install -d ${sysconfdir}/xdg/menus
	install -m 0755 etc/xdg/menus/mom-applications.menu ${sysconfdir}/xdg/menus
	install -d ${sysconfdir}/marchobmenu
	install -m 0755 etc/marchobmenu/* ${sysconfdir}/marchobmenu
	install -d ${prefix}/bin
	install -m 0755 usr/bin/* ${prefix}/bin
	ln -sf -T ${prefix}/lib/marchobmenu/mom-daemon.py ${prefix}/bin/mom-daemon
	ln -sf -T ${prefix}/lib/marchobmenu/mom-places.py ${prefix}/bin/mom-places
	ln -sf -T ${prefix}/lib/marchobmenu/mom-bookmarks.py ${prefix}/bin/mom-bookmarks
	ln -sf -T ${prefix}/lib/marchobmenu/mom-recently-used.py ${prefix}/bin/mom-recently-used

uninstall:
	-rm -rf ${prefix}/lib/marchobmenu
	-rm -rf ${prefix}/share/desktop-directories/mom-*.directory
	-rm -rf ${sysconfdir}/marchobmenu
	-rm -f ${sysconfdir}/xdg/menus/mom-applications.menu
	-rm -f ${prefix}/bin/marchobmenud
	-rm -f ${prefix}/bin/mom-daemon
	-rm -f ${prefix}/bin/mom-places
	-rm -f ${prefix}/bin/mom-bookmarks
