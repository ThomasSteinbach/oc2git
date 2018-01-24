#!/bin/bash

if [ ! -f ./.last_project ]; then
  oc project > .last_project
  exit 0
fi

last_project="$(cat .last_project)"
current_project="$(oc project)"

if [ "$last_project" != "$current_project" ]; then
  echo "It seems you are operating on the wrong project."
  echo "Last time you were $last_project"
  echo "Now you are $current_project"
  echo "If really want to switch to another OpenShift-Project, please delete the '.last_project' file in your working directory."
  exit 1
fi
