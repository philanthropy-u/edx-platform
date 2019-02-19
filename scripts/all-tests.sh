#!/usr/bin/env bash
set -e

###############################################################################
#
#   all-tests.sh
#
#   Execute tests for edx-platform. This script is designed to be the
#   entry point for various CI systems.
#
###############################################################################

# Violations thresholds for failing the build
export PYLINT_THRESHOLD=3600
export ESLINT_THRESHOLD=9850

SAFELINT_THRESHOLDS=`cat scripts/safelint_thresholds.json`
export SAFELINT_THRESHOLDS=${SAFELINT_THRESHOLDS//[[:space:]]/}

# TODO: Determine the CI system for the environment
SCRIPT_TO_RUN=scripts/travis-ci-tests.sh

# Run appropriate CI system script
if [ -n "$SCRIPT_TO_RUN" ] ; then
    $SCRIPT_TO_RUN

    # Exit with the exit code of the called script
    exit $?
else
    echo "ERROR. Could not detect continuous integration system."
    exit 1
fi
