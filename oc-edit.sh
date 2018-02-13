#!/bin/bash

set -e

origin=$(dirname $(readlink -f "$0"))

# check for external changes
"$origin/oc-sync-git.sh" $*

# do edits
oc edit is,cm,pvc,sa,bc,dc,svc,route

# apply current changes
labels="$(cat .labels)"
"$origin/oc-sync-git.sh" $labels
