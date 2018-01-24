set -e

origin=$(dirname $(readlink "$0"))

# check for external changes
"$origin/check-for-changes.sh"

# do edits
oc edit is,cm,pvc,sa,bc,dc,svc,route

# apply current changes
"$origin/check-for-changes.sh"
