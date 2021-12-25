#!/bin/sh
# Assumes the repo has already been cloned in ~
# The cronjob assumes this is run in ~, but the script is written to work from any dir

repo="https://github.com/nglaeser/library-scanner"
# repo must be public for this line to work
url=$(curl -Ls -o /dev/null -w %{url_effective} $repo/releases/latest/)
tag=$(basename $url)
# alternative (uses tags):
# git fetch --tags
# tag=$(git describe --tags `git rev-list --tags --max-count=1`)

cd ~/library-scanner
# pull newest release
git pull origin $tag
# or the following??
# git checkout $tag

# return to previous directory
cd -
cp ~/library-scanner/getlatest.sh .
chmod +x getlatest.sh

# restart scanner script
cd ~/library-scanner
pkill python3
python3 main.py