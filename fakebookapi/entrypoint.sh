#!/bin/sh

echo "Waiting for mysql..."

while ! nc -z web-db 3306; do
  sleep 0.1
done

echo "MySQL started"

exec "$@"
