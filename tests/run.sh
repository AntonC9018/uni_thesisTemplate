set -e
# gets directory of this file
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# goes into the thesis directory with the render script
cd -- "$SCRIPT_DIR/../thesis"
NAME="test.$1"
# must be run there, because config.sty expects to be in the cwd
./render.sh --input="$SCRIPT_DIR/$NAME.tex"
# only works on WSL to open the file in the browser
explorer.exe "$NAME.pdf"
