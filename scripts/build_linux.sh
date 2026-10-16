#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
    echo "Usage: scripts/build_linux.sh X.Y.Z" >&2
    exit 1
fi

if [[ -n "${PYTHON:-}" ]]; then
    PYTHON_CMD="$PYTHON"
elif [[ -x ".venv/bin/python" ]]; then
    PYTHON_CMD=".venv/bin/python"
elif [[ -x "venv/bin/python" ]]; then
    PYTHON_CMD="venv/bin/python"
else
    PYTHON_CMD="python3"
fi

"$PYTHON_CMD" scripts/check_version.py "$VERSION"
"$PYTHON_CMD" -m pip install -r requirements-dev.txt
"$PYTHON_CMD" -m PyInstaller --clean --noconfirm PADOrganizer-linux.spec

APPIMAGE_NAME="PADOrganizer-v${VERSION}-x86_64.AppImage"
DEB_NAME="padorganizer_${VERSION}_amd64.deb"
APPDIR="build/linux/AppDir"
DEB_ROOT="build/linux/deb/padorganizer"

rm -rf "$APPDIR" "$DEB_ROOT"
mkdir -p \
    "$APPDIR/usr/lib/padorganizer" \
    "$APPDIR/usr/bin" \
    "$APPDIR/usr/share/applications" \
    "$APPDIR/usr/share/icons/hicolor/256x256/apps" \
    "$APPDIR/usr/share/icons/hicolor/512x512/apps" \
    "$DEB_ROOT/DEBIAN" \
    "$DEB_ROOT/opt/padorganizer" \
    "$DEB_ROOT/usr/bin" \
    "$DEB_ROOT/usr/share/applications" \
    "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps" \
    "$DEB_ROOT/usr/share/icons/hicolor/512x512/apps" \
    "$DEB_ROOT/usr/share/doc/padorganizer" \
    release

cp -a dist/PADOrganizer/. "$APPDIR/usr/lib/padorganizer/"
install -m 0755 packaging/linux/AppRun "$APPDIR/AppRun"
install -m 0755 packaging/linux/appimage-launcher "$APPDIR/usr/bin/padorganizer"
install -m 0644 packaging/linux/padorganizer.desktop "$APPDIR/padorganizer.desktop"
install -m 0644 packaging/linux/padorganizer.desktop "$APPDIR/usr/share/applications/padorganizer.desktop"
install -m 0644 assets/padorganizer.png "$APPDIR/padorganizer.png"
install -m 0644 assets/padorganizer.png "$APPDIR/usr/share/icons/hicolor/256x256/apps/padorganizer.png"
install -m 0644 assets/padorganizer-512.png "$APPDIR/usr/share/icons/hicolor/512x512/apps/padorganizer.png"
install -m 0644 LICENSE NOTICE "$APPDIR/usr/lib/padorganizer/"

cp -a dist/PADOrganizer/. "$DEB_ROOT/opt/padorganizer/"
install -m 0755 packaging/linux/padorganizer "$DEB_ROOT/usr/bin/padorganizer"
install -m 0644 packaging/linux/padorganizer.desktop "$DEB_ROOT/usr/share/applications/padorganizer.desktop"
install -m 0644 assets/padorganizer.png "$DEB_ROOT/usr/share/icons/hicolor/256x256/apps/padorganizer.png"
install -m 0644 assets/padorganizer-512.png "$DEB_ROOT/usr/share/icons/hicolor/512x512/apps/padorganizer.png"
install -m 0644 LICENSE "$DEB_ROOT/usr/share/doc/padorganizer/copyright"
install -m 0644 NOTICE "$DEB_ROOT/usr/share/doc/padorganizer/NOTICE"
sed "s/@VERSION@/${VERSION}/g" packaging/linux/debian/control > "$DEB_ROOT/DEBIAN/control"
dpkg-deb --build --root-owner-group "$DEB_ROOT" "release/$DEB_NAME"

APPIMAGETOOL_CMD="${APPIMAGETOOL:-appimagetool}"
if ! command -v "$APPIMAGETOOL_CMD" >/dev/null 2>&1 && [[ ! -x "$APPIMAGETOOL_CMD" ]]; then
    echo "appimagetool was not found. Set APPIMAGETOOL to its executable path." >&2
    exit 1
fi

ARCH=x86_64 VERSION="$VERSION" APPIMAGE_EXTRACT_AND_RUN=1 "$APPIMAGETOOL_CMD" \
    --no-appstream "$APPDIR" "release/$APPIMAGE_NAME"
"$PYTHON_CMD" scripts/new_checksums.py release "$DEB_NAME" "$APPIMAGE_NAME"

echo "Linux release v${VERSION} created in release/."
