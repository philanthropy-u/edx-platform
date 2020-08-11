#!/bin/bash
set -e

###############################################################################
#
#   unit-tests.sh
#
#   Execute Python unit tests for edx-platform.
#
#   This script is typically called from generic-ci-tests.sh, which defines
#   these environment variables:
#
#   `TEST_SUITE` defines which kind of test to run.
#   Possible values are:
#
#       - "lms-unit": Run the LMS Python unit tests
#       - "cms-unit": Run the CMS Python unit tests
#       - "commonlib-unit": Run Python unit tests from the common/lib directory
#
#   `SHARD` is a number indicating which subset of the tests to build.
#
#       For "lms-unit", the tests are put into shard groups
#       using the 'attr' decorator (e.g. "@attr(shard=1)"). Anything with
#       the 'shard=n' attribute will run in the nth shard. If there isn't a
#       shard explicitly assigned, the test will run in the last shard.
#
#   This script is broken out so it can be run by tox and redirect stderr to
#   the specified file before tox gets a chance to redirect it to stdout.
#
###############################################################################

export SKIP_NPM_INSTALL="True"

# Skip re-installation of Python prerequisites inside a tox execution.
if [[ -n "$TOXENV" ]]; then
    export NO_PREREQ_INSTALL="True"
fi

if [[ -n "$XDIST_NUM_WORKERS" ]]; then
    bash scripts/xdist/prepare_xdist_nodes.sh
    PAVER_ARGS="-v --xdist_ip_addresses="$(<pytest_worker_ips.txt)""
    export SHARD="all"
    if [[ -n "$XDIST_REMOTE_NUM_PROCESSES" ]]; then
        PARALLEL="--processes=$XDIST_REMOTE_NUM_PROCESSES"
    else
        PARALLEL="--processes=1"
    fi
else
    PAVER_ARGS="-v"
    PARALLEL="--processes=-1"
fi

# declare -a test_suites=(
# "openedx/features/marketplace/tests.py"
# "openedx/features/idea/tests.py"
# )

# for val in ${test_suites[@]}; do
#     paver test_system -s lms -t $val ${PAVER_ARGS} ${PARALLEL} 2> lms-tests.log
# done
# mv reports/.coverage reports/.coverage.lms


case "${TEST_SUITE}" in

    "lms-old-unit")
        case "$SHARD" in
            "all")
                paver test_system -s lms --disable_capture ${PAVER_ARGS} ${PARALLEL} 2> lms-tests.log
                mv reports/.coverage reports/.coverage.lms
                ;;
            [1-9])
                paver test_system -s lms --disable_capture --eval-attr="shard==$SHARD" ${PAVER_ARGS} ${PARALLEL} 2> lms-tests.${SHARD}.log
                mv reports/.coverage reports/.coverage.lms.${SHARD}
                ;;
            10|"noshard")
                paver test_system -s lms --disable_capture --eval-attr="shard>=$SHARD or not shard" ${PAVER_ARGS} ${PARALLEL} 2> lms-tests.10.log
                mv reports/.coverage reports/.coverage.lms.10
                ;;
            *)
                # If no shard is specified, rather than running all tests, create an empty xunit file. This is a
                # backwards compatibility feature. If a new shard (e.g., shard n) is introduced in the build
                # system, but the tests are called with the old code, then builds will not fail because the
                # code is out of date. Instead, there will be an instantly-passing shard.
                mkdir -p reports/lms
                emptyxunit "lms/nosetests"
                ;;
        esac
        ;;

    "cms-unit")
        case "$SHARD" in
            "all")
                paver test_system -s cms --disable_capture ${PAVER_ARGS} ${PARALLEL} 2> cms-tests.log
                mv reports/.coverage reports/.coverage.cms
                ;;
            1)
                paver test_system -s cms --disable_capture --eval-attr="shard==$SHARD" ${PAVER_ARGS} 2> cms-tests.${SHARD}.log
                mv reports/.coverage reports/.coverage.cms.${SHARD}
                ;;
            2|"noshard")
                paver test_system -s cms --disable_capture --eval-attr="shard>=$SHARD or not shard" ${PAVER_ARGS} 2> cms-tests.2.log
                mv reports/.coverage reports/.coverage.cms.2
                ;;
            *)
                # If no shard is specified, rather than running all tests, create an empty xunit file. This is a
                # backwards compatibility feature. If a new shard (e.g., shard n) is introduced in the build
                # system, but the tests are called with the old code, then builds will not fail because the
                # code is out of date. Instead, there will be an instantly-passing shard.
                mkdir -p reports/cms
                emptyxunit "cms/nosetests"
                ;;
        esac
        ;;

    "commonlib-unit")
        case "$SHARD" in
            "all")
                paver test_lib --disable_capture ${PAVER_ARGS} ${PARALLEL} 2> common-tests.log
                mv reports/.coverage reports/.coverage.commonlib
                ;;
            [1-2])
                paver test_lib -l common/lib/xmodule --disable_capture --eval-attr="shard==$SHARD" ${PAVER_ARGS} 2> common-tests.${SHARD}.log
                mv reports/.coverage reports/.coverage.commonlib.${SHARD}
                ;;
            3|"noshard")
                paver test_lib --disable_capture --eval-attr="shard>=$SHARD or not shard" ${PAVER_ARGS} 2> common-tests.3.log
                mv reports/.coverage reports/.coverage.commonlib.3
                ;;
            *)
                # If no shard is specified, rather than running all tests, create an empty xunit file. This is a
                # backwards compatibility feature. If a new shard (e.g., shard n) is introduced in the build
                # system, but the tests are called with the old code, then builds will not fail because the
                # code is out of date. Instead, there will be an instantly-passing shard.
                mkdir -p reports/common
                emptyxunit "common/nosetests"
                ;;
        esac
        ;;

    "lms-unit")
        echo $TEST_DB_NAME
        echo $TEST_DB_USER
        echo $TEST_DB_HOST
        echo $TEST_DB_PASSWORD

        philu_apps_list=(
            "openedx/features/marketplace/"
        )
        # paver test_system -s lms -t openedx/features/marketplace/ -v --processes=1 2> philu-tests.log
        philu_apps_str="${philu_apps_list[@]}"
        paver test_system -s lms -t "${philu_apps_str}" ${PAVER_ARGS} ${PARALLEL} 2> philu-tests.log
        mv reports/.coverage reports/.coverage.philu
esac
