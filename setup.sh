#!/bin/sh
# Keep execution inside a function so a truncated piped download cannot start installation.
main() {
    set -eu
    case "${1:-}" in
        -h|--help)
            echo 'Install globally: curl -fsSL <installer-url> | sh'
            echo 'Install a workspace: curl -fsSL <installer-url> | sh -s -- --workspace "/path"'
            echo 'Re-run the same command to update. CODEX_WORKFLOW_REF selects a revision, default main.'
            return
            ;;
    esac
    for bootstrap_tool in curl tar mktemp; do
        command -v "$bootstrap_tool" >/dev/null 2>&1 || {
            echo "Installation requires $bootstrap_tool." >&2
            exit 1
        }
    done
    bootstrap_tmp=$(mktemp -d "${TMPDIR:-/tmp}/codex-workflows.XXXXXXXX")
    trap 'rm -rf "$bootstrap_tmp"' 0
    trap 'exit 1' HUP INT TERM
    bootstrap_ref=${CODEX_WORKFLOW_REF:-main}
    bootstrap_url=${CODEX_WORKFLOW_ARCHIVE_URL:-https://codeload.github.com/what3verCODE/codex-workflows/tar.gz/$bootstrap_ref}
    echo "Downloading Codex workflow kit..."
    curl -fsSL --retry 2 --connect-timeout 20 --max-time 180 "$bootstrap_url" -o "$bootstrap_tmp/kit.tar.gz"
    mkdir "$bootstrap_tmp/kit"
    tar -xzf "$bootstrap_tmp/kit.tar.gz" -C "$bootstrap_tmp/kit" --strip-components=1
    test -f "$bootstrap_tmp/kit/scripts/install.py" && test -f "$bootstrap_tmp/kit/manifest.json" || {
        echo 'Downloaded archive is missing the workflow installer or manifest.' >&2
        exit 1
    }
    if [ "$#" -eq 0 ]; then
        set -- --global
    fi
    bootstrap_python=${PYTHON:-python3}
    if command -v "$bootstrap_python" >/dev/null 2>&1 &&
        "$bootstrap_python" -c 'import sys; sys.exit(sys.version_info < (3, 11))' >/dev/null 2>&1; then
        "$bootstrap_python" "$bootstrap_tmp/kit/scripts/install.py" "$@"
    else
        echo 'Preparing a temporary Python runtime...'
        curl -fsSL --retry 2 --connect-timeout 20 --max-time 180 https://astral.sh/uv/install.sh -o "$bootstrap_tmp/uv-install.sh"
        UV_UNMANAGED_INSTALL="$bootstrap_tmp/uv" sh "$bootstrap_tmp/uv-install.sh" </dev/null
        UV_PYTHON_INSTALL_DIR="$bootstrap_tmp/python" UV_CACHE_DIR="$bootstrap_tmp/cache" \
            "$bootstrap_tmp/uv/uv" run --no-config --no-project --python 3.12 --managed-python \
            "$bootstrap_tmp/kit/scripts/install.py" "$@"
    fi
    echo 'Codex workflow kit installed. Restart Codex to load the skills and roles.'
}

main "$@"
