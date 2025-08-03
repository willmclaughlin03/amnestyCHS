from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name = 'news_list),'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('admin/create/', views.NewsCreateView.as_view(), name='news_create'),
]