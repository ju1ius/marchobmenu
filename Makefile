package="marchobmenu"
version="1.5"

export prefix=/usr/local
export sysconfdir=/etc

CC=gcc
CFLAGS=-W -Wall -pedantic
LDFLAGS=-linotifytools
EXEC=usr/lib/marchobmenu/mom-watch
SRC=usr/lib/marchobmenu/mom-watch.c

mom-watch:
	${CC} ${SRC} -o ${EXEC} ${LDFLAGS} ${CFLAGS}

.PHONY: clean install uninstall

clean:
	rm ${EXEC}

install:
	install -d ${prefix}/lib/marchobmenu
	install -m 0755 usr/lib/marchobmenu/* ${prefix}/lib/marchobmenu
	install -d ${prefix}/share/desktop-directories
	install -m 0755 usr/share/desktop-directories/* ${prefix}/share/desktop-directories
	install -d ${sysconfdir}/xdg/menus
	install -m 0755 etc/xdg/menus/mom-applications.menu ${sysconfdir}/xdg/menus
	install -d ${sysconfdir}/marchobmenu
	install -m 0755 etc/marchobmenu/* ${sysconfdir}/marchobmenu
	install -d ${prefix}/bin
	ln -s -T ${prefix}/lib/marchobmenu/mom-daemon ${prefix}/bin/mom-daemon
	ln -s -T ${prefix}/lib/marchobmenu/mom-watch ${prefix}/bin/mom-watch

uninstall:
	-rm -rf ${prefix}/lib/marchobmenu
	-rm -rf ${prefix}/share/desktop-directories/mom-*.directory
	-rm -rf ${sysconfdir}/marchobmenu
	-rm -f ${sysconfdir}/xdg/menus/mom-applications.menu
	-rm -f ${prefix}/bin/mom-daemon
	-rm -f ${prefix}/bin/mom-watch
