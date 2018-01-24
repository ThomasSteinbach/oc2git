#!/bin/bash

if [ ! -f ./.last-project ]; then
  oc project > .last-project
  exit 0
fi

last-project=$(cat .last-project)
current-project=$(oc project)

if [ "$last-project" != "$current-project" ]; then
  echo "It seems you are operating on the wrong project."
  echo "Last time you were $last-project"
  echo "Now you are $current-project"
  echo "If really want to switch to another OpenShift-Project, please delete the '.last-project' file in your working directory."
  exit 1
fi
