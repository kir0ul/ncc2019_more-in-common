#!/bin/sh

for file in $(git diff --diff-filter=d --name-only origin/master | grep ".*\.ipynb$"); do

    JUPY=$(jupytext --from ipynb --to py:light --test $file | grep "Cells.*differ")

    if [ -z "${JUPY}" ]
    then
        # If it is empty => everything OK
        echo "Jupytext OK for file": $file
    else
        echo "Jupytext not OK for file": $file
        exit 1
    fi
done
exit 0
