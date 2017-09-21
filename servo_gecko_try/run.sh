#!/usr/bin/env bash
wd=`pwd`
set -e
cd $2 # servo-clone
git fetch origin refs/pull/$1/merge
git diff FETCH_HEAD^ FETCH_HEAD --src-prefix="a/servo/" --dst-prefix="b/servo/" -- . ':(exclude)tests' >${wd}/servo.patch
cd $wd
cd $3 # gecko-clone
hg revert -a
hg qpop -a
hg qdelete servo.patch || true
hg pull -u
hg qimport ${wd}/servo.patch
hg qpush servo.patch
./mach try  -b do -p linux64 -u all -t none