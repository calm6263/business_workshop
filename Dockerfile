# استخدام صورة Python خفيفة
FROM python:3.10-slim

# منع كتابة ملفات pyc وتمكين الإخراج المباشر للسجلات
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# تثبيت الاعتماديات على مستوى النظام (مثل مكتبات Pillow)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات وتثبيت حزم Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# نسخ باقي المشروع
COPY . /app/

# منح صلاحيات التنفيذ لسكربت الدخول
RUN chmod +x /app/entrypoint.sh

# تنفيذ سكربت الدخول عند بدء الحاوية
ENTRYPOINT ["/app/entrypoint.sh"]