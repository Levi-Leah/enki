#!/bin/bash

path_to_script="$(realpath $(dirname "$0"))"
enki=$path_to_script'/src/enki.py'

# install dependencies
pip3 install -qr $path_to_script'/requirements.txt'

sed -i "\|enki\.py|d" ~/.bashrc

echo 'alias enki="python3 '$enki'"' >> ~/.bashrc
source ~/.bashrc
