#!/bin/bash

path_to_script="$(realpath $(dirname "$0"))"
enki=$path_to_script'/src/enki.py'

# install dependencies
pip install -r $path_to_script'/requirements.txt'

if [ "grep enki.py ~/.bashrc" ]; then
    sed -i "\|enki.py|d" ~/.bashrc
fi

echo 'alias lcheck="python3 '$enki'"' >> ~/.bashrc
source ~/.bashrc
