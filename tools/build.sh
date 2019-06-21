#!/bin/bash
set -e

export MOC_ADJUTANT_VERSION=r4

docker build . --build-arg IMAGE=fedora:30 -t "massopencloud/adjutant-moc:$MOC_ADJUTANT_VERSION"
docker tag "massopencloud/adjutant-moc:$MOC_ADJUTANT_VERSION" "massopencloud/adjutant-moc:$MOC_ADJUTANT_VERSION-amd64"
# docker build . --build-arg IMAGE=ppc64le/fedora:30 -t "massopencloud/adjutant-moc:$MOC_ADJUTANT_VERSION-ppc64le"
