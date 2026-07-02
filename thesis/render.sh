#!/usr/bin/env bash
set -o errexit -o noclobber -o nounset

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd -- "$script_dir/.." && pwd)"
texlive_bin="/usr/local/texlive/2025/bin/x86_64-linux"
render_venv="${THESIS_RENDER_VENV:-$repo_dir/.render-venv}"
render_requirements="$script_dir/render-requirements.txt"
render_requirements_stamp="$render_venv/.requirements-installed"

find_render_python() {
    if [ -n "${THESIS_RENDER_PYTHON:-}" ]; then
        printf '%s\n' "$THESIS_RENDER_PYTHON"
        return
    fi

    if command -v python3.14 > /dev/null 2>&1; then
        printf '%s\n' python3.14
        return
    fi

    if command -v python3 > /dev/null 2>&1; then
        printf '%s\n' python3
        return
    fi

    echo "render.sh: python3.14 or python3 is required" >&2
    exit 5
}

setup_render_venv() {
    if [ ! -f "$render_requirements" ]; then
        echo "render.sh: missing $render_requirements" >&2
        exit 5
    fi

    if [ ! -x "$render_venv/bin/python" ]; then
        mkdir -p -- "$(dirname -- "$render_venv")"
        "$(find_render_python)" -m venv "$render_venv"
    fi

    if [ ! -f "$render_requirements_stamp" ] \
        || [ "$render_requirements" -nt "$render_requirements_stamp" ]; then
        "$render_venv/bin/python" -m pip install \
            --disable-pip-version-check \
            -r "$render_requirements"
        touch "$render_requirements_stamp"
    fi
}

LONGOPTS=force,input:
OPTS=f
PARSED=$(getopt --options=$OPTS --longoptions=$LONGOPTS --name "$0" -- "$@") || exit 2
eval set -- "$PARSED"

force=n
input=main.tex
while true; do
    case "$1" in 
        -f|--force)
            force=y
            shift
            ;;
        --input)
            input="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error"
            exit 3
            ;;
    esac
done

if [ "$force" = "y" ]; then
    git clean -Xfd
fi

setup_render_venv

# Hardcode TeX Live in case the user didn't export it before. Prepend the
# render venv so LaTeX shell-escape resolves python3 and pygmentize from it.
export VIRTUAL_ENV="$render_venv"
export PATH="$render_venv/bin:$PATH:$texlive_bin"

'latexmk' '--shell-escape' '-xelatex' "$input"

log_file="${input%.tex}.log"
if [ -f "$log_file" ] && grep -q "CONFIG_VISIBLE_WARNING" "$log_file"; then
    echo "render.sh: visible warning found in $log_file" >&2
    exit 4
fi
