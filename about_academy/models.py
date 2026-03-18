from django.db import models
from django.core.validators import FileExtensionValidator

class ValuesSection(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок", default="Наши ценности")
    rocket_image = models.ImageField(upload_to='about_academy/values/', blank=True, null=True,
                                   verbose_name="Изображение ракеты")
    quote_1 = models.TextField(verbose_name="Цитата 1", 
                              default="Мы создаем свободное пространство для идей и развития, помогая проявить достаточно смелости, чтобы воплотить их в жизнь с верой в себя.")
    quote_2 = models.TextField(verbose_name="Цитата 2",
                              default="Наша уникальность заключается в объединении четырех школ: Академии Аристотеля, Майевтики Сократа, Мастерской да Винчи и Методики воспитания силы воли Сеченова.")
    content = models.TextField(verbose_name="Дополнительный контент", blank=True)
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    show_dot = models.BooleanField(default=True, verbose_name="Показывать точку")
    show_arrow = models.BooleanField(default=True, verbose_name="Показывать стрелку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Раздел 'Наши ценности'"
        verbose_name_plural = "Разделы 'Наши ценности'"
        ordering = ['order']
    
    def __str__(self):
        return self.title


class StatisticsSection(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок", default="Академия в цифрах")
    stat_title = models.CharField(max_length=200, verbose_name="Заголовок статистики", default="К образовательным программам")
    
    stat_number_1 = models.CharField(max_length=50, verbose_name="Число 1", default="20 000")
    stat_label_1 = models.CharField(max_length=200, verbose_name="Подпись 1", default="Тысяч выпущенных учеников")
    
    stat_number_2 = models.CharField(max_length=50, verbose_name="Число 2", default="380")
    stat_label_2 = models.CharField(max_length=200, verbose_name="Подпись 2", default="Телефонных звонков")
    
    stat_number_3 = models.CharField(max_length=50, verbose_name="Число 3", default="983")
    stat_label_3 = models.CharField(max_length=200, verbose_name="Подпись 3", default="Котят")
    
    content = models.TextField(verbose_name="Дополнительный контент", blank=True)
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    show_dot = models.BooleanField(default=True, verbose_name="Показывать точку")
    show_arrow = models.BooleanField(default=True, verbose_name="Показывать стрелку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Раздел 'Академия в цифрах'"
        verbose_name_plural = "Разделы 'Академия в цифрах'"
        ordering = ['order']
    
    def __str__(self):
        return self.title


class PhotoAlbum(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название альбома")
    cover_image = models.ImageField(upload_to='about_academy/albums/covers/', 
                                  verbose_name="Обложка альбома")
    description = models.TextField(blank=True, verbose_name="Описание альбома")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Фотоальбом"
        verbose_name_plural = "Фотоальбомы"
        ordering = ['order']
    
    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, 
                             related_name='images', verbose_name="Альбом", default=1)
    image = models.ImageField(
        upload_to='about_academy/gallery/%Y/%m/%d/',
        verbose_name="Изображение",
        help_text="Можно выбрать несколько файлов одновременно"
    )
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фотографии"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Фото {self.id}"


class LeaderSpeech(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок", default="Речь руководителя")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Речь руководителя"
        verbose_name_plural = "Речь руководителя"
        ordering = ['order']
    
    def __str__(self):
        return self.title


class LeaderSpeechVideo(models.Model):
    leader_speech = models.ForeignKey(LeaderSpeech, on_delete=models.CASCADE, 
                                    related_name='videos', verbose_name="Речь руководителя")
    title = models.CharField(max_length=200, verbose_name="Название видео")
    video_url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True, 
                               help_text="Ссылка на YouTube или другое видео (необязательно, если загружаете файл)")
    video_file = models.FileField(
        upload_to='leader_speech/videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'])],
        blank=True,
        null=True,
        verbose_name="Видео файл",
        help_text="Загрузите видео файл (MP4, AVI, MOV, WMV, FLV, WEBM)"
    )
    thumbnail = models.ImageField(upload_to='leader_speech/thumbnails/', blank=True, null=True,
                                verbose_name="Превью видео")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Видео речи руководителя"
        verbose_name_plural = "Видео речи руководителя"
        ordering = ['order']
    
    def __str__(self):
        return self.title
    
    def get_video_source(self):
        if self.video_file:
            return self.video_file.url
        return self.video_url


class MainSlider(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок слайда", blank=True)
    description = models.TextField(verbose_name="Описание слайда", blank=True)
    image = models.ImageField(upload_to='main_slider/', verbose_name="Изображение слайда")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Слайд главной страницы"
        verbose_name_plural = "Слайды главной страницы"
        ordering = ['order']
    
    def __str__(self):
        return self.title or f"Слайд {self.id}"


class DownloadableFile(models.Model):
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('word', 'Word'),
        ('powerpoint', 'PowerPoint'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название файла", default="Презентация")
    description = models.TextField(verbose_name="Описание файла", blank=True)
    file_type = models.CharField(max_length=15, choices=FILE_TYPES, default='pdf',
                               verbose_name="Тип файла")
    file = models.FileField(
        upload_to='downloadable_files/',
        verbose_name="Файл",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'xlsx', 'xls', 'docx', 'doc', 'pptx', 'ppt'])],
        help_text="Загрузите файл PDF, Excel, Word или PowerPoint"
    )
    button_text = models.CharField(max_length=100, verbose_name="Текст кнопки", 
                                 default="Скачать презентацию")
    button_color = models.CharField(max_length=7, default="#7F1726", 
                                  verbose_name="Цвет кнопки",
                                  help_text="Введите HEX-код цвета (пример: #7F1726)")
    text_color = models.CharField(max_length=7, default="#FDFDFD", 
                                verbose_name="Цвет текста",
                                help_text="Введите HEX-код цвета (пример: #FDFDFD)")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    position_right = models.BooleanField(default=True, verbose_name="Позиция справа")
    show_icon = models.BooleanField(default=True, verbose_name="Показывать иконку")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Файл для скачивания"
        verbose_name_plural = "Файлы для скачивания"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title
    
    def get_file_icon(self):
        icons = {
            'pdf': 'fa-file-pdf',
            'excel': 'fa-file-excel',
            'word': 'fa-file-word',
            'powerpoint': 'fa-file-powerpoint',
        }
        return icons.get(self.file_type, 'fa-file-download')
    
    def get_file_extension(self):
        return self.file_type.upper()


class Leadership(models.Model):
    name = models.CharField(max_length=200, verbose_name="ФИО")
    position = models.TextField(verbose_name="Должность (можно с переносами)")
    image = models.ImageField(upload_to='about_academy/leadership/', verbose_name="Фото")
    description = models.TextField(verbose_name="Описание", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(max_length=50, verbose_name="Телефон", blank=True)
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Руководитель"
        verbose_name_plural = "Руководство"
        ordering = ['order']

    def __str__(self):
        return self.name


class QuoteSection(models.Model):
    title = models.CharField(
        max_length=200, 
        verbose_name="Заголовок", 
        default="Цитата"
    )
    quote_text = models.TextField(
        verbose_name="Текст цитаты"
    )
    image = models.ImageField(
        upload_to='about_academy/quotes/', 
        blank=True, 
        null=True, 
        verbose_name="Изображение"
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Активно"
    )
    order = models.IntegerField(
        default=0, 
        verbose_name="Порядок"
    )

    class Meta:
        verbose_name = "Цитата (под ценностями)"
        verbose_name_plural = "Цитаты (под ценностями)"
        ordering = ['order']

    def __str__(self):
        return self.title


# ===== NEW MODEL FOR ACADEMY TEAM (Команда) =====
from departments.models import Department   # تأكد من وجود هذا التطبيق

class AcademyTeamMember(models.Model):
    RANK_CHOICES = [
        ('director', 'Директор'),
        ('deputy_director', 'Заместитель директора'),
        ('teacher', 'Преподаватель'),
        ('employee', 'Сотрудник'),
    ]

    name = models.CharField(max_length=200, verbose_name="ФИО")
    image = models.ImageField(upload_to='about_academy/team/', verbose_name="Фото")
    position = models.TextField(verbose_name="Должность (можно с переносами)")
    description = models.TextField(blank=True, verbose_name="Описание")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Телефон")

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='academy_team_members',
        verbose_name="Отделение"
    )
    rank = models.CharField(max_length=20, choices=RANK_CHOICES, default='employee', verbose_name="Иерархический ранг")

    order = models.IntegerField(default=0, verbose_name="Порядок внутри ранга")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Член команды (Об академии)"
        verbose_name_plural = "Члены команды (Об академии)"
        ordering = ['department', 'rank', 'order']

    def __str__(self):
        return self.name