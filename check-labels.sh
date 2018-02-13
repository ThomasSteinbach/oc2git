#!/bin/bash

if [ ! -f ./.labels ]; then
  echo "$*" > .labels
  exit 0
fi

last_labels="$(cat .labels)"
current_labels="$*"

if [ "$last_labels" != "$current_labels" ]; then

  if [ "$current_labels" == '' ]; then
    echo "Do you want to operate on you last set of labels used:"
    echo "$last_labels"
    read -p '(y/n): ' answer

    if [ "${answer,,}" == 'y' ]; then
      exit 0
    fi
  fi

  echo "It seems you are operating on a different set of labels than last time."
  echo "Last time you were using: $last_labels"
  echo "Now you are using: $current_labels"
  echo "If really want to switch the set of labels, please delete the '.labels' file in your working directory."
  exit 1
fi
