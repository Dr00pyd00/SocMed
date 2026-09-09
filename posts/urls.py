
from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
        path('test/', views.test_view, name='posts-test'),
        path('create/', views.create_post, name='post-creation'),
        path('<int:pk>/', views.detail_post, name='post-detail'),


        ]
