ARG BASE_IMAGE=base/netternotes:latest
FROM ${BASE_IMAGE}

ARG SERVICE_PORT=8000
ENV SERVICE_PORT=${SERVICE_PORT}

# copy sources and entrypoint file to service home
COPY netternotes.py ${SERVICE_HOME}/netternotes.py
COPY init_db.py ${SERVICE_HOME}/init_db.py
COPY templates/* ${SERVICE_HOME}/templates/
COPY static/* ${SERVICE_HOME}/static/
COPY entrypoint.sh /entrypoint.sh

RUN chown ${SERVICE_NAME} ${SERVICE_HOME}
RUN chmod u+rw ${SERVICE_HOME}
RUN chmod +x /entrypoint.sh

# define user and workdir
WORKDIR ${SERVICE_HOME}
USER ${SERVICE_NAME}

# run entrypoint script
ENTRYPOINT /entrypoint.sh