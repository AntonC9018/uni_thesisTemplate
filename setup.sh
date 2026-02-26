set -e

sudo apt update
sudo apt install perl python3

if [ -d temp ]; then
    rm -rf temp
fi

mkdir temp
repo_dir="$PWD"
temp_dir="$repo_dir/temp"

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
export_cmd='export PATH=/usr/local/texlive/2025/bin/x86_64-linux:$PATH'
echo "$export_cmd" >> ~/.bashrc
eval "$export_cmd"

# Fonts
cd -- "$repo_dir"
sudo apt install fonts-liberation
sudo cp fonts/*.ttf /usr/share/fonts/
fc-cache -f -v
