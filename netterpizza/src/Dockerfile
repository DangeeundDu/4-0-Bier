ARG BASE_IMAGE=base/netterpizza:latest
FROM ${BASE_IMAGE}

LABEL description="Run image for the netterpizza service"
ARG SERVICE_PORT=8333
ARG SERVICE_NAME=netterpizza
ENV SERVICE_PORT=${SERVICE_PORT}
ENV SERVICE_NAME=${SERVICE_NAME}

# copy the source to the service home
COPY backend ${SERVICE_HOME}/backend
COPY www ${SERVICE_HOME}/www
COPY site /etc/apache2/sites-available/netterpizza.conf

RUN a2ensite netterpizza \
    && echo "Listen 8333" > /etc/apache2/ports.conf \
    && mkdir -p /var/log/netterpizza /tmp/apache2run /tmp/apache2lock \
    && chown "root:${SERVICE_NAME}" /var/log/netterpizza /tmp/apache2run /tmp/apache2lock \
    && chmod 770 /var/log/netterpizza /tmp/apache2run /tmp/apache2lock \
    && cd $SERVICE_HOME/backend \
    && make

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
ENV APACHE_LOG_DIR     /var/log/netterpizza
ENV LANG               C

CMD /bin/bash -c 'touch ${SERVICE_HOME}/db/{000..449}/userdata; apache2 -D FOREGROUND'
