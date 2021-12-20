#!/bin/sh

# test repo
# repo="https://github.com/nglaeser/graph_cyclone"
repo="https://github.com/nglaeser/library-scanner"
url=$(curl -Ls -o /dev/null -w %{url_effective} $repo/releases/latest)
tag=$(basename $url)
git pull origin $tag

# restart script
pkill Python
python main.py