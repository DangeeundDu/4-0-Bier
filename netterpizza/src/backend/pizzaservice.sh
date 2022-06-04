#!/bin/sh
cd /app/db
exec /app/backend/pizzaservice "$@"

