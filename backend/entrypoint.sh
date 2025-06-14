#!/bin/sh
# entrypoint.sh

echo "Starting cron…"
/usr/sbin/cron

echo "Switching to appuser and starting Gunicorn…"
exec runuser -u appuser -- gunicorn --bind 0.0.0.0:8000 --workers 3 f1hub.wsgi:application
