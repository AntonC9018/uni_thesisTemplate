#!/usr/bin/env bash
set -euo pipefail

file_uri() {
    python3 - "$1" <<'PY'
from pathlib import Path
import sys

print(Path(sys.argv[1]).resolve().as_uri())
PY
}

is_wsl() {
    grep -qiE '(microsoft|wsl)' /proc/version 2>/dev/null
}

open_windows_browser() {
    local windows_path=$1

    powershell.exe -NoProfile -NonInteractive -Command '& {
        param([string]$path)

        $ErrorActionPreference = "Stop"
        $uri = [System.Uri]::new($path).AbsoluteUri
        foreach ($browser in @("msedge.exe", "chrome.exe", "firefox.exe")) {
            $command = Get-Command $browser -ErrorAction SilentlyContinue
            if ($command) {
                Start-Process -FilePath $command.Source -ArgumentList $uri
                exit 0
            }
        }
        Start-Process $uri
    }' "$windows_path"
}

pdf_path=${1:-}
[ -n "$pdf_path" ] || exit 1
[ -f "$pdf_path" ] || exit 1

if is_wsl && command -v wslpath >/dev/null 2>&1 && command -v powershell.exe >/dev/null 2>&1; then
    temp_dir="$(
        powershell.exe -NoProfile -NonInteractive -Command '[System.IO.Path]::GetTempPath()' 2>/dev/null \
            | tr -d '\r' \
            | sed -n '1{s/[[:space:]]*$//;p;}'
    )"

    if [ -n "$temp_dir" ]; then
        temp_dir="$(wslpath -u "$temp_dir")/uni-thesis-template-vscode"
        mkdir -p "$temp_dir"
        temp_pdf="$temp_dir/$(basename -- "$pdf_path")"
        cp -f -- "$pdf_path" "$temp_pdf"
        windows_path="$(wslpath -w "$temp_pdf")"
    else
        windows_path="$(wslpath -w "$pdf_path")"
    fi

    open_windows_browser "$windows_path" || true
    exit 0
fi

if command -v python3 >/dev/null 2>&1; then
    uri="$(file_uri "$pdf_path")"
    if python3 - "$uri" <<'PY'
import sys
import webbrowser

raise SystemExit(0 if webbrowser.open_new_tab(sys.argv[1]) else 1)
PY
    then
        exit 0
    fi
fi

if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$pdf_path" >/dev/null 2>&1 || true
    exit 0
fi

if command -v open >/dev/null 2>&1; then
    open "$pdf_path" >/dev/null 2>&1 || true
    exit 0
fi

exit 0
