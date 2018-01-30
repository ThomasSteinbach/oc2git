#!/bin/bash

oc status &>/dev/null
retVal=$?
if [ $retVal -ne 0 ]; then
  echo "Please login to OpenShift first."
  exit 0
fi

if [ ! -f .last_project ] || [ ! -f api-objects.yaml ]; then
  echo 'This script is meant to be run within repositories'
  echo 'created with oc-edit or oc-sync-git.'
  exit 0
fi

old_project="$(sed -E 's/^Using project "(.*)" on.*$/\1/' .last_project)"
current_project="$(oc project | sed -E 's/^Using project "(.*)" on.*$/\1/')"

if [ "$current_project" != "$old_project" ]; then
  echo "The current project (${current_project}) differs from the project name (${old_project})"
  echo "where the API objects were exported from."

  read -p "Do you want to import all API objects into the project ${current_project}? (y/n)" answer

  if [ "${answer,,}" != 'y' ]; then
    exit 0
  fi

  ASK_FOR_PROJECT_CHANGE=true
fi

sed "s/OC_PROJECT_NAME/${current_project}/g" api-objects.yaml | oc apply -f -

if [ ! -z "$ASK_FOR_PROJECT_CHANGE" ]; then
  read -p "Do you want to write the new project name to this repository? (y/n)" switchproj
  if [ "${switchproj,,}" == 'y' ]; then
    oc project > .last_project
  fi
fi
