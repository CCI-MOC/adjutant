#!/bin/bash
docker push massopencloud/adjutant-moc:r1
docker push massopencloud/adjutant-moc:r1-amd64
docker push massopencloud/adjutant-moc:r1-ppc64le

docker manifest create massopencloud/adjutant-moc:r1 \
    massopencloud/adjutant-moc:r1-amd64 \
    massopencloud/adjutant-moc:r1-ppc64le --amend

docker manifest push massopencloud/adjutant-moc:r1