#!/usr/bin/env bash

dot "$1".dot | gvpr -c -f binarytree.gvpr | neato -n -Tpng -o $1.png