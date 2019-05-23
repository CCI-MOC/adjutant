ARG IMAGE
FROM $IMAGE

LABEL author="Kristi Nikolla <knikolla@bu.edu>"

ENV PBR_VERSION 0.1

RUN dnf install -y gcc mariadb-devel python3-devel libffi-devel openssl-devel

COPY --chown=1001:0 . /app
RUN pip3 install -U pip setuptools && \
    pip3 install /app

# Note(knikolla): This is required to support the random
# user IDs that OpenShift enforces.
# https://docs.openshift.com/enterprise/3.2/creating_images/guidelines.html
RUN chmod -R g+rwX /app

EXPOSE 8080

USER 1001

ENTRYPOINT [ "/app/run_adjutant.sh" ]
