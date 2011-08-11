# Contributor: David Spicer <azleifel at googlemail dot diddly dot dot com>

pkgname=marchobmenu-git
pkgver=20100313
pkgrel=1
pkgdesc="An Openbox automated XDG Menu"
arch=('any')
url="http://github.com/ju1ius/marchobmenu"
license=('GPL')
depends=('openbox' 'bash' 'libinotifytools0' 'python-xdg>=0.19')
makedepends=('git' 'libinotifytools0-dev')
provides=('marchobmenu')
conflicts=('marchobmenu')

_gitroot="git://github.com/ju1ius/marchobmenu.git"
_gitname="marchobmenu"

build() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [ -d $_gitname ] ; then
    cd $_gitname
    git pull
    msg "The local files are updated."
  else
    git clone $_gitroot $_gitname
  fi

  msg "GIT checkout done or server timeout"

  msg "Starting make..."
  cd "$srcdir/$_gitname"
  make || return 1
  sudo make install
}

