#!/usr/bin/env bash
export SECRET_KEY=`uuidgen`

cd /app

cp conf/conf.moc.yml conf/conf.yaml
sed -i -e "
    s|%SECRET_KEY%|$SECRET_KEY|g;
    s|%DB_USER%|$DB_USER|g;
    s|%DB_PASSWORD%|$DB_PASSWORD|g;
    s|%OPENSTACK_AUTH_URL%|$OPENSTACK_AUTH_URL|g;
    s|%OPENSTACK_USERNAME%|$OPENSTACK_USERNAME|g;
    s|%OPENSTACK_PASSWORD%|$OPENSTACK_PASSWORD|g;
    s|%OPENSTACK_PROJECT%|$OPENSTACK_PROJECT|g;
    s|%EMAIL_HOST%|$EMAIL_HOST|g;
    s|%EMAIL_USERNAME%|$EMAIL_USERNAME|g;
    s|%EMAIL_PASSWORD%|$EMAIL_PASSWORD|g;
    " conf/conf.yaml

adjutant-api migrate
adjutant-api runserver 0.0.0.0:8080
