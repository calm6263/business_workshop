from django.urls import reverse_lazy

from news.models import News, Category, NewsPageHero, Subscriber
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- News ----------------------
class NewsListView(BaseAdminListView):
    model = News
    template_name = 'dashboards/crud/news/news_list.html'
    context_object_name = 'items'
    paginate_by = 20

class NewsCreateView(BaseAdminCreateView):
    model = News
    fields = ['title', 'slug', 'content', 'image', 'category', 'publish_date', 'is_active']
    template_name = 'dashboards/crud/news/news_form.html'
    success_url = reverse_lazy('dashboards:news_list')
    success_message = "Новость успешно добавлена"

class NewsUpdateView(BaseAdminUpdateView):
    model = News
    fields = ['title', 'slug', 'content', 'image', 'category', 'publish_date', 'is_active']
    template_name = 'dashboards/crud/news/news_form.html'
    success_url = reverse_lazy('dashboards:news_list')
    success_message = "Новость успешно обновлена"

class NewsDeleteView(BaseAdminDeleteView):
    model = News
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:news_list')
    success_message = "Новость удалена"

# ---------------------- Category ----------------------
class CategoryListView(BaseAdminListView):
    model = Category
    template_name = 'dashboards/crud/news/category_list.html'
    context_object_name = 'items'

class CategoryCreateView(BaseAdminCreateView):
    model = Category
    fields = ['name', 'slug']
    template_name = 'dashboards/crud/news/category_form.html'
    success_url = reverse_lazy('dashboards:category_list')
    success_message = "Категория добавлена"

class CategoryUpdateView(BaseAdminUpdateView):
    model = Category
    fields = ['name', 'slug']
    template_name = 'dashboards/crud/news/category_form.html'
    success_url = reverse_lazy('dashboards:category_list')
    success_message = "Категория обновлена"

class CategoryDeleteView(BaseAdminDeleteView):
    model = Category
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:category_list')
    success_message = "Категория удалена"

# ---------------------- NewsPageHero ----------------------
class NewsPageHeroListView(BaseAdminListView):
    model = NewsPageHero
    template_name = 'dashboards/crud/news/newspagehero_list.html'
    context_object_name = 'items'

class NewsPageHeroCreateView(BaseAdminCreateView):
    model = NewsPageHero
    fields = ['title', 'subtitle', 'image', 'is_active', 'show_button', 'button_text', 'button_link', 'order']
    template_name = 'dashboards/crud/news/newspagehero_form.html'
    success_url = reverse_lazy('dashboards:newspagehero_list')
    success_message = "Баннер добавлен"

class NewsPageHeroUpdateView(BaseAdminUpdateView):
    model = NewsPageHero
    fields = ['title', 'subtitle', 'image', 'is_active', 'show_button', 'button_text', 'button_link', 'order']
    template_name = 'dashboards/crud/news/newspagehero_form.html'
    success_url = reverse_lazy('dashboards:newspagehero_list')
    success_message = "Баннер обновлен"

class NewsPageHeroDeleteView(BaseAdminDeleteView):
    model = NewsPageHero
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:newspagehero_list')
    success_message = "Баннер удален"

# ---------------------- Subscriber ----------------------
class SubscriberListView(BaseAdminListView):
    model = Subscriber
    template_name = 'dashboards/crud/news/subscriber_list.html'
    context_object_name = 'items'
    paginate_by = 20

class SubscriberCreateView(BaseAdminCreateView):
    model = Subscriber
    fields = ['email', 'consent', 'is_active']
    template_name = 'dashboards/crud/news/subscriber_form.html'
    success_url = reverse_lazy('dashboards:subscriber_list')
    success_message = "Подписчик добавлен"

class SubscriberUpdateView(BaseAdminUpdateView):
    model = Subscriber
    fields = ['email', 'consent', 'is_active']
    template_name = 'dashboards/crud/news/subscriber_form.html'
    success_url = reverse_lazy('dashboards:subscriber_list')
    success_message = "Подписчик обновлен"

class SubscriberDeleteView(BaseAdminDeleteView):
    model = Subscriber
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:subscriber_list')
    success_message = "Подписчик удален"