#!/bin/bash
set -e

cd "$(dirname "$0")"

IP="${EXTERNAL_IP}"
DEPLOYDIR="${SERVICE_HOME}/deploy/home/www"
SOURCEDIR="${SERVICE_HOME}/files/home/www"

if [[ ! -d $DEPLOYDIR ]]; then
  mkdir -p $DEPLOYDIR
  cp -r $SOURCEDIR/* $DEPLOYDIR/

  [[ -z "$IP" ]] && IP=$(hostname -I | awk '{ print $1 }')

  echo "Personalizing landing page, our external IP is: $IP"
  find $DEPLOYDIR/ -type f -name '*.html' | xargs sed -i -re "s,##IP##,$IP,g"
  chown -R ${SERVICE_USER}:${SERVICE_USER} $DEPLOYDIR
fi

/usr/sbin/lighttpd -t -f ${SERVICE_HOME}/${SERVICE_NAME}.conf

exec /usr/sbin/lighttpd -D -f ${SERVICE_HOME}/${SERVICE_NAME}.conf
