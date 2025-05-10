#!/bin/bash
find templates -type f -exec ./render.sh "{}" \;
cp -r assets site
cp -r static site
