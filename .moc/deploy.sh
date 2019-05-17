#! /bin/bash
oc apply -f specs/adjutant-secret.yaml
oc apply -f specs/adjutant.yaml
oc apply -f specs/adjutant-route.yaml