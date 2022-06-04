ARG BASE_IMAGE=base/landing-page:latest

FROM ${BASE_IMAGE}

LABEL description="Run image for the landing page"
ARG SERVICE_PORT=8080
ENV SERVICE_PORT=${SERVICE_PORT}

# copy source files to service host
COPY files ${SERVICE_HOME}/files
COPY ${SERVICE_NAME}.conf ${SERVICE_HOME}/${SERVICE_NAME}.conf
COPY entrypoint.sh /entrypoint.sh

# expose some ports
EXPOSE ${SERVICE_PORT}

# define execution user and entry point
USER ${SERVICE_NAME}
CMD [ "/entrypoint.sh" ]
