#!/bin/bash

PORT=${PORT:-5804}
THREADS=${THREADS:-7}
PRELOAD=${PRELOAD:--preload}

gunicorn \
    --bind=0.0.0.0:${PORT} \
    --worker-class=gthread \
    --threads=${THREADS} \
    --workers=1 \
    --access-logfile - \
    --timeout=6000 \
    "${PRELOAD}" \
    backend.api:app