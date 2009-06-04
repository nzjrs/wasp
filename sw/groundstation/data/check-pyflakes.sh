#!/bin/sh
for f in `find . -type f \( -name "*.py" \)`
do
    pyflakes $f
done

