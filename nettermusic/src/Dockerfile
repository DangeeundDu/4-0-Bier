ARG BASE_IMAGE=base/nettermusic:latest

FROM ${BASE_IMAGE}

LABEL description="Run image for the nettermusic service"
ARG SERVICE_PORT=9000
ARG SERVICE_NAME=nettermusic
ENV SERVICE_PORT=${SERVICE_PORT}
ENV SERVICE_NAME=${SERVICE_NAME}

COPY site /etc/apache2/sites-available/nettermusic.conf
COPY index.html exec.php create.php delete.php list.php play.php nettermusic.png nettermusicstyle.css secure_validator.pas ${SERVICE_HOME}/

RUN a2ensite nettermusic \
    && echo "Listen 9000" > /etc/apache2/ports.conf \
    && mkdir -p /var/log/nettermusic /tmp/apache2run /tmp/apache2lock /data/store \
    && chown "root:${SERVICE_NAME}" /var/log/nettermusic /tmp/apache2run /tmp/apache2lock /data/store \
    && chmod 770 /var/log/nettermusic /tmp/apache2run /tmp/apache2lock /data/store

WORKDIR ${SERVICE_HOME}

# Compile secure validator
RUN fpc secure_validator.pas

# expose some ports
EXPOSE ${SERVICE_PORT}

# define execution user and entry point
USER ${SERVICE_NAME}:${SERVICE_NAME}

ENV APACHE_RUN_USER    ${SERVICE_NAME}
ENV APACHE_RUN_GROUP   ${SERVICE_NAME}
ENV APACHE_PID_FILE    /tmp/apache2.pid
ENV APACHE_RUN_DIR     /tmp/apache2run
ENV APACHE_LOCK_DIR    /tmp/apache2lock
ENV APACHE_LOG_DIR     /var/log/nettermusic
ENV LANG               C

CMD apache2 -D FOREGROUND