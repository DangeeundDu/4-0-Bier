ARG BASE_IMAGE=base/nettermaps:latest
FROM ${BASE_IMAGE}

LABEL description="Run image for the nettermaps service"
ARG SERVICE_PORT=8495
ARG SERVICE_NAME=nettermaps
ENV SERVICE_PORT=${SERVICE_PORT}
ENV SERVICE_NAME=${SERVICE_NAME}

# copy the source to the service home
COPY www ${SERVICE_HOME}
COPY site /etc/apache2/sites-available/maps.conf
# COPY php.ini /etc/php/7.0/apache2/php.ini
RUN a2ensite maps \
    && echo "Listen 8495" > /etc/apache2/ports.conf \
    && mkdir -p /var/log/maps /tmp/apache2run /tmp/apache2lock /data/store \
    && chown "root:${SERVICE_NAME}" /var/log/maps /tmp/apache2run /tmp/apache2lock /data/store \
    && chmod 770 /var/log/maps /tmp/apache2run /tmp/apache2lock /data/store

WORKDIR ${SERVICE_HOME}
# expose some ports
EXPOSE ${SERVICE_PORT}

# define execution user and entry point
USER ${SERVICE_NAME}:${SERVICE_NAME}

ENV APACHE_RUN_USER    ${SERVICE_NAME}
ENV APACHE_RUN_GROUP   ${SERVICE_NAME}
ENV APACHE_PID_FILE    /tmp/apache2.pid
ENV APACHE_RUN_DIR     /tmp/apache2run
ENV APACHE_LOCK_DIR    /tmp/apache2lock
ENV APACHE_LOG_DIR     /var/log/maps
ENV LANG               C

CMD apache2 -D FOREGROUND
