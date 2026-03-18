from django.db import models
import hashlib

class ContactMessage(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    email = models.EmailField(verbose_name="E-mail")
    message = models.TextField(verbose_name="Сообщение")
    is_robot = models.BooleanField(default=False, verbose_name="Я не робот")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    email_hash = models.CharField(max_length=64, blank=True, null=True, verbose_name="Хеш email")
    client_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP адрес")
    user_agent = models.TextField(blank=True, null=True, verbose_name="User Agent")
    
    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email_hash', 'created_at']),
            models.Index(fields=['client_ip', 'created_at']),
        ]
    
    def __str__(self):
        return f"Сообщение от {self.name} ({self.email})"
    
    def save(self, *args, **kwargs):
        # إنشاء هاش للبريد الإلكتروني لتجنب تخزينه بشكل مباشر عند التحقق من التكرار
        if self.email:
            self.email_hash = hashlib.sha256(self.email.lower().encode()).hexdigest()
        super().save(*args, **kwargs)