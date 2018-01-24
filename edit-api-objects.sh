set -e

export EDITOR=vim

# check for external changes
./check-for-changes.sh

# do edits
oc edit is,cm,pvc,sa,bc,dc,svc,route

# apply current changes
./check-for-changes.sh
