#!/usr/bin/env bash
set -euo pipefail

die() {
    printf 'VS Code thesis render: %s\n' "$*" >&2
    exit 1
}

start_pdf_opener() {
    local pdf_path=$1
    local opener_script=$2

    "$opener_script" "$pdf_path" >/dev/null 2>&1 || true
}

render_args=()
while [ "$#" -gt 0 ]; do
    case "$1" in
        -f|--force)
            render_args+=(--force)
            shift
            ;;
        *)
            break
            ;;
    esac
done

active_file=${1:-}
[ -n "$active_file" ] || die "open a .tex file inside thesis/ and press F5."
[ -f "$active_file" ] || die "active file does not exist: $active_file"
if [ "$#" -gt 1 ]; then
    die "unexpected arguments after active file: ${*:2}"
fi

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
workspace_dir="$(cd -- "$script_dir/.." && pwd -P)"
thesis_dir="$workspace_dir/thesis"

[ -d "$thesis_dir" ] || die "thesis directory not found: $thesis_dir"
[ -x "$thesis_dir/render.sh" ] || die "render script is not executable: $thesis_dir/render.sh"

active_file="$(realpath -- "$active_file")"
thesis_dir="$(realpath -- "$thesis_dir")"

case "$active_file" in
    *.tex) ;;
    *) die "active file is not a .tex file: $active_file" ;;
esac

relative_input="$(realpath --relative-to="$thesis_dir" "$active_file")"
case "$relative_input" in
    ..|../*|/*)
        die "active file must be inside $thesis_dir"
        ;;
esac

cd -- "$thesis_dir"
set +e
./render.sh "${render_args[@]}" --input "$relative_input"
render_status=$?
set -e

if [ "$render_status" -ne 0 ] && [ "$render_status" -ne 4 ]; then
    exit "$render_status"
fi

pdf_path="$thesis_dir/${relative_input%.tex}.pdf"
[ -f "$pdf_path" ] || die "render completed, but no PDF was found at $pdf_path"

printf 'Built PDF: %s\n' "$pdf_path"

if [ "${THESIS_VSCODE_NO_BROWSER:-}" = "1" ]; then
    if [ "$render_status" -eq 4 ]; then
        exit 0
    fi

    exit "$render_status"
fi

opener_script="$script_dir/open-pdf.sh"
[ -x "$opener_script" ] || die "PDF opener script is not executable: $opener_script"
start_pdf_opener "$pdf_path" "$opener_script"
if [ "$render_status" -eq 4 ]; then
    exit 0
fi

exit "$render_status"
