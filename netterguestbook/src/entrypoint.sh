#!/bin/bash
set -e
python3 -c "import random;print(random.random())" > secret
gunicorn --worker-tmp-dir=/dev/shm --workers=4 --threads=8 --log-file=- --bind=0.0.0.0:9999 netterguestbook:app
