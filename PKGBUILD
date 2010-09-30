# Contributor: David Spicer <azleifel at googlemail dot diddly dot dot com>

pkgname=marchobmenu-git
pkgver=20100313
pkgrel=1
pkgdesc="An Openbox automated XDG Menu"
arch=('any')
url="http://github.com/ju1ius/marchobmenu"
license=('GPL')
depends=('openbox' 'bash' 'inotify-tools' 'python-xdg>=0.19')
makedepends=('git')
provides=('marchobmenu')
conflicts=('marchobmenu')

_gitroot="git://github.com/ju1ius/marchobmenu.git"
_gitname="marchobmenu"

build() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [ -d $_gitname ] ; then
    cd $_gitname && git pull origin
    msg "The local files are updated."
  else
    git clone $_gitroot $_gitname
  fi

  msg "GIT checkout done or server timeout"

  msg "Starting make..."
  cd "$srcdir/$_gitname/usr/lib/marchobmenu"
  make || return 1

  cd "$srcdir/$_gitname"

  install -d -m755 "$pkgdir/usr/lib" || return 1
  cp -Rp "usr/lib/marchobmenu" "$pkgdir/usr/lib" || return 1
  install -d m755 "$pkgdir/usr/bin" || return 1
  cp -p "usr/bin/*" "$pkgdir/usr/bin"
  install -d -m755 "$pkgdir/etc/xdg/menus" || return 1
  cp -p "etc/xdg/menus/mom-applications.menu" "$pkgdir/etc/xdg/menus" || return 1
  install -d -m755 "$pkgdir/usr/share" || return 1
  cp -Rp "usr/share/desktop-directories" "$pkgdir/usr/share" || return 1
  install -D -m644 "README.md" "$pkgdir/usr/share/doc/marchobmenu/README" || return 1
}

