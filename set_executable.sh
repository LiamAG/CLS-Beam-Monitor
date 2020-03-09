#!/bin/sh
# change the directory below into the targeted directory
DIR="C:\Users\Marte\PycharmProjects\Capstone"
inotifywait -m -r -e move -e create --format '%w%f' "$DIR" | while read f

do
  python ImageExample.py
done