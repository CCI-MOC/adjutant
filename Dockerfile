FROM fedora:30

LABEL author="Kristi Nikolla <knikolla@bu.edu>"

ENV PBR_VERSION 0.1

# Bug https://bugzilla.redhat.com/show_bug.cgi?id=1694411
RUN echo "zchunk=False" >> /etc/dnf/dnf.conf && \
    dnf install -y gcc python3-devel python3 python3-pip \
        libffi-devel openssl-devel mariadb mariadb-devel

COPY --chown=1001:0 . /app
RUN pip3 install /app

# Note(knikolla): This is required to support the random
# user IDs that OpenShift enforces.
# https://docs.openshift.com/enterprise/3.2/creating_images/guidelines.html
RUN chmod -R g+rwX /app

EXPOSE 8080

USER 1001

ENTRYPOINT [ "/app/run_adjutant.sh" ]
