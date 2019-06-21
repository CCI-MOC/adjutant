#!/usr/bin/env bash
set -e

cd /app

cp conf/conf.moc.yml conf/conf.yaml
sed -i -e "
    s|%SECRET_KEY%|$SECRET_KEY|g;
    s|%DB_HOST%|$DB_HOST|g;
    s|%DB_USER%|$DB_USER|g;
    s|%DB_PASSWORD%|$DB_PASSWORD|g;
    s|%OPENSTACK_AUTH_URL%|$OPENSTACK_AUTH_URL|g;
    s|%OPENSTACK_USERNAME%|$OPENSTACK_USERNAME|g;
    s|%OPENSTACK_PASSWORD%|$OPENSTACK_PASSWORD|g;
    s|%OPENSTACK_PROJECT%|$OPENSTACK_PROJECT|g;
    s|%EMAIL_HOST%|$EMAIL_HOST|g;
    s|%EMAIL_PORT%|$EMAIL_PORT|g;
    s|%EMAIL_USERNAME%|$EMAIL_USERNAME|g;
    s|%EMAIL_PASSWORD%|$EMAIL_PASSWORD|g;
    s|%PUBLIC_NETWORK_ID%|$PUBLIC_NETWORK_ID|g;
    " conf/conf.yaml

while ! mysqladmin ping -h $DB_HOST --silent; do
    >&2 echo "Waiting for database"
    sleep 1
done

>&2 echo "Database is up - Starting"

adjutant-api migrate
adjutant-api runserver 0.0.0.0:8080
