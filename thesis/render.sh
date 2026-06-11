#!/usr/bin/env bash
set -o errexit -o noclobber -o nounset

LONGOPTS=force,input:
OPTS=f
PARSED=$(getopt --options=$OPTS --longoptions=$LONGOPTS --name "$0" -- "$@") || exit 2
eval set -- "$PARSED"

# Just hardcode this in case the user didn't export it before
export PATH=$PATH:/usr/local/texlive/2025/bin/x86_64-linux

force=n, input=main.tex
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
'latexmk' '--shell-escape' '-xelatex' "$input"
