
from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
        path('create/', views.create_post, name='post-creation'),
        path('<int:pk>/', views.detail_post, name='post-detail'),
        path('<int:pk>/update', views.update_post, name='post-update'),
        path('mines/', views.get_all_user_posts, name='post-mines-list'),
        path('feed/', views.feed_posts, name='post-feed'),
        path('<int:pk>/delete', views.delete_post, name='post-delete'),



       ]
