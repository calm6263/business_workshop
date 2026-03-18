# dashboards/urls/crud_news_urls.py
from django.urls import path
from ..views import crud_news

urlpatterns = [
    # News
    path('news/', crud_news.NewsListView.as_view(), name='news_list'),
    path('news/add/', crud_news.NewsCreateView.as_view(), name='news_add'),
    path('news/<int:pk>/edit/', crud_news.NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', crud_news.NewsDeleteView.as_view(), name='news_delete'),

    # Category
    path('categories/', crud_news.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', crud_news.CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', crud_news.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', crud_news.CategoryDeleteView.as_view(), name='category_delete'),

    # NewsPageHero
    path('hero/', crud_news.NewsPageHeroListView.as_view(), name='newspagehero_list'),
    path('hero/add/', crud_news.NewsPageHeroCreateView.as_view(), name='newspagehero_add'),
    path('hero/<int:pk>/edit/', crud_news.NewsPageHeroUpdateView.as_view(), name='newspagehero_edit'),
    path('hero/<int:pk>/delete/', crud_news.NewsPageHeroDeleteView.as_view(), name='newspagehero_delete'),

    # Subscriber
    path('subscribers/', crud_news.SubscriberListView.as_view(), name='subscriber_list'),
    path('subscribers/add/', crud_news.SubscriberCreateView.as_view(), name='subscriber_add'),
    path('subscribers/<int:pk>/edit/', crud_news.SubscriberUpdateView.as_view(), name='subscriber_edit'),
    path('subscribers/<int:pk>/delete/', crud_news.SubscriberDeleteView.as_view(), name='subscriber_delete'),
]