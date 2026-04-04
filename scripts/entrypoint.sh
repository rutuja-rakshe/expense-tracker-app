#!/bin/sh
set -e

echo "==> Waiting for database..."
python -c "
import time, os, psycopg2
db_url = os.environ.get('DATABASE_URL', '')
for i in range(30):
    try:
        if db_url:
            psycopg2.connect(db_url)
        else:
            psycopg2.connect(
                host=os.environ.get('DB_HOST','localhost'),
                port=os.environ.get('DB_PORT','5432'),
                dbname=os.environ.get('DB_NAME','expense_tracker'),
                user=os.environ.get('DB_USER','postgres'),
                password=os.environ.get('DB_PASSWORD',''),
            )
        print('DB ready.')
        break
    except Exception as e:
        print(f'Attempt {i+1}/30 — waiting... ({e})')
        time.sleep(2)
else:
    print('Could not connect to DB. Exiting.')
    exit(1)
"

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Starting server..."
exec "$@"