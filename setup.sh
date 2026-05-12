#!/usr/bin/env bash

texlive_bin="/usr/local/texlive/2025/bin/x86_64-linux"
(
    set -euo pipefail

    # Ask for sudo password once at the beginning
    sudo -v

    # Keep sudo alive during long TeX Live install
    while true; do
        sudo -n true
        sleep 60
    done 2>/dev/null &
    sudo_keepalive_pid=$!

    trap 'kill $sudo_keepalive_pid' EXIT

    sudo apt update
    sudo apt install -y perl python3 wget tar fonts-liberation fontconfig

    repo_dir="$PWD"
    temp_dir="$repo_dir/temp"

    cd -- "$temp_dir"

    if [ -d "$texlive_bin" ]; then
        echo "TeX Live already installed, skipping."
    else
        rm -rf -- "$temp_dir"
        mkdir -p -- "$temp_dir"

        wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
        tar -xzf install-tl-unx.tar.gz

        set -- install-tl-*/
        cd -- "$1"

cat <<EOF > "$temp_dir/texlive.profile"
selected_scheme scheme-full
TEXDIR /usr/local/texlive/2025
TEXMFCONFIG $HOME/.texlive2025/texmf-config
TEXMFVAR $HOME/.texlive2025/texmf-var
option_doc 0
option_src 0
EOF

        sudo perl ./install-tl -profile "$temp_dir/texlive.profile"
    fi

    # Fonts
    cd -- "$repo_dir"

    sudo cp -- fonts/*.ttf /usr/share/fonts/
    fc-cache -f -v

    echo
    echo "Setup complete."
)

export_cmd="export PATH=$texlive_bin:\$PATH"
if ! grep -qxF "$export_cmd" "$HOME/.bashrc"; then
    echo "$export_cmd" >> "$HOME/.bashrc"
fi
eval "$export_cmd"
