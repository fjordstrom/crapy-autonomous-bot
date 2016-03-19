#!/bin/bash

if [ "$1" ]; then
	find $1 -iname "*.vec" > $1".txt"
else
	echo "Folder name required"
fi