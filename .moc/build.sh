#!/bin/bash
cd ..

docker build . --build-arg IMAGE=fedora:29 -t massopencloud/adjutant-moc:r1
docker tag massopencloud/adjutant-moc:r1 massopencloud/adjutant-moc:r1-amd64
docker build . --build-arg IMAGE=ppc64le/fedora:29 -t massopencloud/adjutant-moc:r1-ppc64le

cd .moc