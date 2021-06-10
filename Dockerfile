# This will produce an image to be used in Openshift
# Build should be triggered from repo root like:
# docker build -f Dockerfile --tag <IMAGE_TAG>

FROM registry.fedoraproject.org/fedora:32
LABEL \
    name="ResultsDB_frontend application" \
    vendor="ResultsDB_frontend developers" \
    license="GPLv2+" \
    description="ResultsDB_frontend is a simple application that allows browsing the data stored inside ResultsDB." \
    usage="" \
    build-date=""

USER root

ARG DEFAULT_LOG_LEVEL=info
ENV LOG_LEVEL=$DEFAULT_LOG_LEVEL
COPY ./resultsdb_frontend.spec /opt/app-root/src/resultsdb_frontend/resultsdb_frontend.spec

# install dependencies defined in RPM spec file
RUN dnf -y install findutils rpm-build python3-pip python3-mod_wsgi httpd \
    && rpm --query --requires --specfile /opt/app-root/src/resultsdb_frontend/resultsdb_frontend.spec | xargs -d '\n' dnf -y install \
    && dnf -y clean all
 
COPY . /opt/app-root/src/resultsdb_frontend/
# install using --no-deps option to ensure nothing comes from PyPi
RUN pip3 install --no-deps /opt/app-root/src/resultsdb_frontend

# fix apache config for container use
RUN sed -i 's#^WSGISocketPrefix .*#WSGISocketPrefix /tmp/wsgi#' /opt/app-root/src/resultsdb_frontend/conf/resultsdb_frontend.conf

# config files
RUN install -d /usr/share/resultsdb_frontend/conf \
    && install -p -m 0644 /opt/app-root/src/resultsdb_frontend/conf/resultsdb_frontend.conf /usr/share/resultsdb_frontend/conf/ \
    && install -p -m 0644 /opt/app-root/src/resultsdb_frontend/conf/resultsdb_frontend.wsgi /usr/share/resultsdb_frontend/ \
    && install -d /etc/resultsdb_frontend \
    && install -p -m 0644 /opt/app-root/src/resultsdb_frontend/conf/resultsdb_frontend.conf /etc/httpd/conf.d/

EXPOSE 5002

CMD ["mod_wsgi-express-3", "start-server", "/usr/share/resultsdb_frontend/resultsdb_frontend.wsgi", \
    "--user", "apache", "--group", "apache", \
    "--port", "5002", "--threads", "5", \
    "--include-file", "/etc/httpd/conf.d/resultsdb_frontend.conf", \
    "--log-level", "${LOG_LEVEL}", \
    "--log-to-terminal", \
    "--access-log", \
    "--startup-log" \
]
USER 1001:0
