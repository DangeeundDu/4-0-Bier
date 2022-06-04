ARG BASE_IMAGE=base/netterguestbook:latest

FROM ${BASE_IMAGE}

COPY entrypoint.sh /entrypoint.sh
COPY netterguestbook.py init_db.py ${SERVICE_HOME}/
COPY templates/* ${SERVICE_HOME}/templates/

USER ${SERVICE_NAME}
WORKDIR ${SERVICE_HOME}

RUN python3 ${SERVICE_HOME}/init_db.py
ENTRYPOINT /entrypoint.sh
