FROM centos/python-36-centos7

LABEL author="Kristi Knikolla <knikolla@bu.edu>"

ENV PBR_VERSION 0.1

COPY --chown=1001:0 . /app
RUN pip install -U pip setuptools && \
    pip install /app

# Note(knikolla): This is required to support the random
# user IDs that OpenShift enforces.
# https://docs.openshift.com/enterprise/3.2/creating_images/guidelines.html
RUN chmod -R g+rwX /app

EXPOSE 8080

USER 1001

ENTRYPOINT [ "/app/run_adjutant.sh" ]
