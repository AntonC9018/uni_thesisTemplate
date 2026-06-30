#!/usr/bin/env bash

set -euo pipefail

die() {
    echo "error: $*" >&2
    exit 1
}

is_wsl() {
    [ -r /proc/sys/kernel/osrelease ] &&
        grep -qiE '(microsoft|wsl)' /proc/sys/kernel/osrelease
}

ensure_wsl_conf() {
    local input_file="$1"
    local output_file="$2"

    awk '
        function flush_interop() {
            if (in_interop) {
                if (!have_enabled) {
                    print "enabled=true"
                }
                if (!have_append_windows_path) {
                    print "appendWindowsPath=true"
                }
            }
        }

        BEGIN {
            in_interop = 0
            seen_interop = 0
            have_enabled = 0
            have_append_windows_path = 0
        }

        /^\[[^]]+\][[:space:]]*$/ {
            flush_interop()

            section = tolower($0)
            sub(/[[:space:]]*$/, "", section)
            in_interop = section == "[interop]"
            if (in_interop) {
                seen_interop = 1
                have_enabled = 0
                have_append_windows_path = 0
            }

            print
            next
        }

        in_interop && tolower($0) ~ /^[[:space:]]*enabled[[:space:]]*=/ {
            print "enabled=true"
            have_enabled = 1
            next
        }

        in_interop &&
            tolower($0) ~ /^[[:space:]]*appendwindowspath[[:space:]]*=/ {
            print "appendWindowsPath=true"
            have_append_windows_path = 1
            next
        }

        {
            print
        }

        END {
            flush_interop()

            if (!seen_interop) {
                if (NR > 0) {
                    print ""
                }
                print "[interop]"
                print "enabled=true"
                print "appendWindowsPath=true"
            }
        }
    ' "$input_file" > "$output_file"
}

windows_where() {
    local executable_name="$1"
    local windows_cmd="/mnt/c/Windows/System32/cmd.exe"
    local windows_path

    [ -f "$windows_cmd" ] || return 1
    command -v wslpath >/dev/null 2>&1 || return 1

    windows_path="$(
        "$windows_cmd" /C "where $executable_name" 2>/dev/null |
            tr -d '\r' |
            sed -n '1p' ||
            true
    )"
    [ -n "$windows_path" ] || return 1

    wslpath -u "$windows_path"
}

find_windows_gcm() {
    local gcm_path
    local candidate
    local candidates=(
        "/mnt/c/Program Files/Git/mingw64/bin/git-credential-manager.exe"
        "/mnt/c/Program Files/Git/usr/bin/git-credential-manager.exe"
        "/mnt/c/Program Files/Git/mingw64/bin/git-credential-manager-core.exe"
    )

    if gcm_path="$(windows_where git-credential-manager.exe)" &&
        [ -f "$gcm_path" ]; then
        printf '%s\n' "$gcm_path"
        return 0
    fi

    if gcm_path="$(windows_where git-credential-manager-core.exe)" &&
        [ -f "$gcm_path" ]; then
        printf '%s\n' "$gcm_path"
        return 0
    fi

    for candidate in "${candidates[@]}"; do
        if [ -f "$candidate" ]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done

    return 1
}

escape_git_helper_path() {
    printf '%q' "$1"
}

main() {
    is_wsl || die "this script only works inside WSL"
    command -v git >/dev/null 2>&1 || die "git is required"
    command -v sudo >/dev/null 2>&1 ||
        die "sudo is required to edit /etc/wsl.conf"

    sudo -v

    input_wsl_conf="$(mktemp)"
    output_wsl_conf="$(mktemp)"
    trap 'rm -f -- "$input_wsl_conf" "$output_wsl_conf"' EXIT

    if [ -f /etc/wsl.conf ]; then
        sudo cat /etc/wsl.conf > "$input_wsl_conf"
    else
        : > "$input_wsl_conf"
    fi

    ensure_wsl_conf "$input_wsl_conf" "$output_wsl_conf"

    wsl_conf_changed=0
    if cmp -s "$input_wsl_conf" "$output_wsl_conf"; then
        echo "/etc/wsl.conf already contains the required interop settings."
    else
        sudo install -m 0644 "$output_wsl_conf" /etc/wsl.conf
        wsl_conf_changed=1
        echo "Updated /etc/wsl.conf with the required interop settings."
    fi

    gcm_path="$(find_windows_gcm)" ||
        die "could not find Windows Git Credential Manager"
    git_helper="$(escape_git_helper_path "$gcm_path")"

    git config --global --replace-all credential.helper "$git_helper"
    echo "Configured Git to use Windows Git Credential Manager:"
    echo "  $gcm_path"

    if [ "$wsl_conf_changed" -eq 1 ]; then
        echo
        echo "Restart WSL from Windows for /etc/wsl.conf changes to take effect:"
        echo "  wsl.exe --shutdown"
    fi
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    main "$@"
fi
