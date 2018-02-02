#!/bin/bash

set -e

origin=$(dirname $(readlink -f "$0"))

# check if user is in wrong project
"$origin/check-project.sh"

# check for changes
oc export is,cm,pvc,sa,bc,dc,svc,route > api-objects.tmp
retVal=$?

if [ $retVal -eq 0 ]; then
  mv api-objects.tmp api-objects.yaml
else
  rm api-objects.tmp
  exit 1
fi

projectname="$(sed -E 's/^Using project "(.*)" on.*$/\1/' .last_project)"
python "${origin}/fixDockerUrls.py" api-objects.yaml "$projectname"

if [[ $(git status --porcelain api-objects.yaml) ]]; then
  git diff -U20
  git add api-objects.yaml .last_project README_oc2git.md
  git commit
fi

cp "${origin}/README_oc2git.md" .
