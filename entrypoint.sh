#!/bin/bash
set -e

PUID=${PUID:-0}
PGID=${PGID:-0}

getent group app &>/dev/null  || groupadd -og ${PGID} app
getent passwd app &>/dev/null || useradd -og ${PGID} -M -d /config -u ${PUID} app

mkdir -p /config
chown -R app:app /config

su -s /bin/bash app <<EOF
cd /app
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - run:app
EOF
