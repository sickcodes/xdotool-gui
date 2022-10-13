_basename=xdotoolgui
pkgname=xdotool-gui
pkgver=1.3
pkgrel=1
pkgdesc="GUI for command-line X11 automation tool"
arch=('any')
url="https://github.com/aleritty/xdotool-gui"
license=('GPL')
makedepends=('git')
depends=('xdotool' 'python3' 'gobject-introspection-runtime' 'python-gobject') #'PyGObject for python
source=("git+https://github.com/aleritty/xdotool-gui")

package() {
  cd "xdotool-gui"

  install -Dm755 xdotoolgui.py "$pkgdir/usr/share/$pkgname/xdotoolgui.py"
  install -Dm644 xdotoolgui.glade "$pkgdir/usr/share/$pkgname/xdotoolgui.glade"
  install -Dm644 xdotoolgui.png "$pkgdir/usr/share/$pkgname/xdotoolgui.png"
  install -Dm 755 xdotool-gui "$pkgdir/usr/local/bin/xdotool-gui"
  install -Dm644 "xdotoolgui.desktop" "$pkgdir/usr/share/applications/xdotoolgui.desktop"
}
sha256sums=('SKIP')