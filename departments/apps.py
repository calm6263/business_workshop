# departments/apps.py
from django.apps import AppConfig

class DepartmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'departments'

    def ready(self):
        # يمكن إضافة الإشارات هنا لاحقاً بعد حل مشكلة الاستيراد الدائري
        pass