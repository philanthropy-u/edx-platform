#!/bin/bash

##
## Pylint Git Pre-commit Hook
##
## Supports linting only staged files, or otherwise defaults to all changed files.
## Add this script in `.git/hooks/pre-commit`.

staged=`git diff --name-only --cached --diff-filter=A --diff-filter=M | cat`
pylint=".venv/bin/pylint --rcfile .pylintrc --load-plugins pylint_django --load-plugins pylint_quotes --reports=no"

if [ "$staged" ]
then
  target=`cat "$staged" | grep '.py$'`
else
  target=`git diff --name-only | cat | grep '.py'`
fi

if [ "$target" ]
then
  docker-compose exec lms bash -c 'source /edx/app/edxapp/edxapp_env && cd /edx/app/edxapp/edx-platform && pylint $target'
fi
