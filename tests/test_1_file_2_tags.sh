#!/bin/bash

if [ -z "$1" ]; then
    echo "ERROR! Usage: $0 </path/to/new/git/repository>"
    exit 1
fi

ORIGINAL_PATH=$(pwd)
REPO_PATH=$1

mkdir -p "$REPO_PATH"
cd "$REPO_PATH"
git init

echo -e 'a = 4, 2\nb = 3,4\n' > first_file.py # 2 lines, 1 with error
git add first_file.py
git commit -m 'first commit'

git tag -a -m 'version 0.1.0' '0.1.0'

echo -e 'c=5,6' >> first_file.py # 3 lines, 2 with errors
git add first_file.py
git commit -m 'second commit'

echo -e 'd = 7,8' >> first_file.py # 4 lines, 3 with errors
git add first_file.py
git commit -m 'third commit'

git tag -a -m 'version 0.1.1' '0.1.1'

echo -e 'e = 8, 9' >> first_file.py # 5 lines, 3 with errors
git add first_file.py
git commit -m 'fourth commit'

cd "$ORIGINAL_PATH"
