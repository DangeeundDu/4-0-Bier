#!/bin/bash
set -e
python3 ../app/init_db.py
gunicorn netternotes:app --worker-tmp-dir=/dev/shm --workers=4 --threads=8 --log-file=- --bind=0.0.0.0:8000 --limit-request-line 8190