#!/usr/bin/env bash
set -e

cd ${TRAVIS_BUILD_DIR}/.travis-ci/playbooks

pip install --user ansible
ansible-playbook -i hosts.ini install.yml

tail devstacklog.txt

cd ${TRAVIS_BUILD_DIR}/travis-ci

docker-compose up -d
