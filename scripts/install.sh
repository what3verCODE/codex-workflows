#!/bin/sh
set -eu
installer_python=${PYTHON:-python3}
if ! command -v "$installer_python" >/dev/null 2>&1; then
    echo "Installation requires Python 3.11 or newer. Install it, then rerun make install." >&2
    exit 1
fi
if ! "$installer_python" -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then
    echo "Installation requires Python 3.11 or newer." >&2
    exit 1
fi
installer_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "$installer_python" "$installer_dir/install.py" "$@"
