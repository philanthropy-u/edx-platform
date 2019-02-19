#!/usr/bin/env bash

###############################################################################
#
#   travis-ci-tests.sh
#
#   Execute tests for edx-platform on travis-ci.org
#
#   Forks should configure parallelism, and use this script
#   to define which tests to run in each of the containers.
#
###############################################################################

# From the sh(1) man page of FreeBSD:
# Exit immediately if any untested command fails. in non-interactive
# mode.  The exit status of a command is considered to be explicitly
# tested if the command is part of the list used to control an if,
# elif, while, or until; if the command is the left hand operand of
# an “&&” or “||” operator; or if the command is a pipeline preceded
# by the ! operator.  If a shell function is executed and its exit
# status is explicitly tested, all commands of the function are con‐
# sidered to be tested as well.
set -e

# Return status is that of the last command to fail in a
# piped command, or a zero if they all succeed.
set -o pipefail

# There is no need to install the prereqs
export NO_PREREQ_INSTALL='true'

EXIT=0

if [ "$CI_NODE_TOTAL" == "1" ] ; then
    echo "Only 1 container is being used to run the tests."

    echo "Running python tests for openedx/features/course_cards"
    paver test_system -t openedx/features/course_card/tests --fasttest --cov-args="-p" --with-xunitmp || EXIT=1

    exit $EXIT
else
    # Split up the tests to run in parallel on 4 containers
    case $CI_NODE_INDEX in
        0)  # run the quality metrics
            echo "Finding pep8 violations and storing report..."
            paver run_pep8 > pep8.log || { cat pep8.log; EXIT=1; }

            mkdir -p reports
            PATH=$PATH:node_modules/.bin

            # Run quality task. Pass in the 'fail-under' percentage to diff-quality
            paver run_quality -p 90 || EXIT=1

            # TODO: paver run_eslint
            # TODO: paver run_pylint
            # TODO: paver run_complexity
            exit $EXIT
            ;;

        1)  # run all of the tests
            echo "Running python tests for openedx/features/course_card"
            paver test_system -t openedx/features/course_card/tests --fasttest --cov-args="-p"
            ;;

    esac
fi
