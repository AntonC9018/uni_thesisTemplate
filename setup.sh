set -e

sudo apt update
sudo apt install perl

if [ -d temp ]; then
    rm -rf temp
fi

mkdir temp
temp_dir="$PWD/temp"

# Latex
cd -- "$temp_dir"
wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
tar -xzf install-tl-unx.tar.gz
set -- install-tl-*/
cd $1
cat <<'EOF' > "$temp_dir/texlive.profile"
selected_scheme scheme-full
TEXDIR /usr/local/texlive/2025
TEXMFCONFIG ~/.texlive2025/texmf-config
TEXMFVAR ~/.texlive2025/texmf-var
option_doc 0
option_src 0
EOF
sudo perl ./install-tl -profile "$temp_dir/texlive.profile"
echo 'export PATH=/usr/local/texlive/2025/bin/x86_64-linux:$PATH' >> ~/.bashrc

# Fonts
cd -- "$temp_dir"
sudo apt install fonts-liberation xz-utils
curl -L -O https://notabug.org/ArtikusHG/times-new-roman/raw/master/times.tar.xz
sudo tar -xf times.tar.xz -C /usr/share/fonts/
fc-cache -f -v
