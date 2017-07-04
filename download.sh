#!/usr/bin/env bash
#-*- coding:utf-8 -*-

./install-deps.sh

./KGraber.py

mkdir -p songs
cd songs
rm *

wait

while read playurl title; do
    wget "$playurl" -O "$title"
done < ../playlist.txt

echo "your musics has been downloaded under the songs directory!"
