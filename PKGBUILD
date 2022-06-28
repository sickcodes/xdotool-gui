_basename=xdotoolgui
pkgname=xdotool-gui-py3 # FIXME
pkgver=1.2
_pkgrel=1
pkgrel=2
pkgdesc="GUI for command-line X11 automation tool"
arch=('any')
url="https://github.com/sickcodes/xdotool-gui"
license=('GPL')
depends=('xdotool' 'python3' 'gobject-introspection' 'python-gobject')
source=(
  "http://downloads.sourceforge.net/project/${pkgname}/${_basename}_${pkgver}-${_pkgrel}.tar.gz" # FIXME
  xdotoolgui.desktop
)

build() {
  cd "$srcdir/$_basename-$pkgver"

  sed -i -re "1s/python2?/python2/" *.py # FIXME
  sed -i -re "44s|sys.path\[0\]|'/usr/share/xdotool-gui'|" xdotoolgui.py # FIXME
}

package() {
  cd "$srcdir/$_basename-$pkgver"
  
  install -Dm755 xdotoolgui.py "$pkgdir/usr/bin/xdotool-gui"
  install -Dm644 xdotoolgui.glade "$pkgdir/usr/share/$pkgname/xdotoolgui.glade"
  install -Dm644 "$srcdir/xdotoolgui.desktop" "$pkgdir/usr/share/applications/xdotoolgui.desktop"
  install -Dm644 data/xdotoolgui.gif "$pkgdir/usr/share/$pkgname/xdotoolgui.gif"
}

# vim:set ts=2 sw=2 et:
md5sums=('SKIP'
         'SKIP') # FIXME