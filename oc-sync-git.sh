#!/bin/bash

set -e

origin=$(dirname $(readlink -f "$0"))

# check if user is in wrong project
"$origin/check-project.sh"

# update .labels file, which labels to use
"$origin/check-labels.sh" $*
labels="$(cat .labels)"

# check for changes
if [ "$labels" == "" ]; then
  oc export is,cm,pvc,sa,bc,dc,svc,route > api-objects.tmp
else
  oc export is,cm,pvc,sa,bc,dc,svc,route -l $labels > api-objects.tmp
fi
retVal=$?

if [ $retVal -eq 0 ]; then
  mv api-objects.tmp api-objects.yaml
else
  rm api-objects.tmp
  exit 1
fi

projectname="$(sed -E 's/^Using project "(.*)" on.*$/\1/' .last_project)"
python "${origin}/fixDockerUrls.py" api-objects.yaml "$projectname"

cp "${origin}/README_oc2git.md" .

if [[ $(git status --porcelain api-objects.yaml) ]]; then
  git diff -U20
  git add api-objects.yaml README_oc2git.md .last_project .labels
  git commit
fi
