#!/usr/bin/env bash
set -e

source ${HOME}/devstack/openrc admin admin

cd ${TRAVIS_BUILD_DIR}/.travis-ci/
py.test tests/

cd ${TRAVIS_BUILD_DIR}
