#!/bin/sh
# Assumes the repo has already been cloned in ~
# The cronjob assumes this is run in ~, but the script is written to work from any dir

repo="https://github.com/nglaeser/library-scanner"
url=$(curl -Ls -o /dev/null -w %{url_effective} $repo/releases/latest)
tag=$(basename $url)

cd ~/library-scanner
# pull newest release
git pull origin $tag
# return to previous directory
cd -
# cp ~/library-scanner/getlatest.sh .
# chmod +x getlatest.sh
# restart scanner script
pkill python
python main.py