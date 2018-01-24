set -e

origin=$(dirname $(readlink "$0"))

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

python "${origin}/fixDockerUrls.py" api-objects.yaml

if [[ $(git status --porcelain) ]]; then
  git diff -U20
  git add api-objects.yaml
  git commit
fi
