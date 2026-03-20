# dashboards/forms.py
from django import forms
from about_academy.models import GalleryImage, PhotoAlbum
from django.forms import inlineformset_factory

# Formset لإدارة الصور الموجودة (بدون حقل image لأن الصور الجديدة ترفع عبر حقل منفصل)
GalleryImageFormSet = inlineformset_factory(
    PhotoAlbum,
    GalleryImage,
    fields=['order', 'is_active'],   # تعديل order و is_active فقط
    extra=0,
    can_delete=True,
)