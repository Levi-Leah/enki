#!/bin/bash

path_to_script="$(realpath $(dirname "$0"))"
enki=$path_to_script'/src/enki.py'

# install ruby
sudo dnf install ruby
sudo dnf install pip


# install dependencies
if test -f $path_to_script'/requirements.txt'; then
    echo 'installing python dependencies'
    pip3 install -qr $path_to_script'/requirements.txt'
fi

if test -f $path_to_script'/Gemfile'; then
    sudo gem install bundler
    bundle install
    echo 'installing ruby dependencies'
    bundle install
fi

sed -i "\|enki\.py|d" ~/.bashrc

echo 'alias enki="python3 '$enki'"' >> ~/.bashrc
source ~/.bashrc
