#!/bin/sh

# تطبيق الهجرات على قاعدة البيانات
echo "Running migrations..."
python manage.py migrate --noinput

# جمع الملفات الثابتة
echo "Collecting static files..."
python manage.py collectstatic --noinput

# تشغيل الخادم باستخدام gunicorn
echo "Starting Gunicorn..."
exec gunicorn business_workshop.wsgi:application --bind 0.0.0.0:8000