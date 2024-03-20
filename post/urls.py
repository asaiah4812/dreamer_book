from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('post-create/', views.post_create, name='post_create'),
    path('post-delete/<str:pk>/', views.post_delete, name='post_delete'),
    path('post-edit/<str:pk>/', views.post_edit, name='post_edit'),
    path('post-page/<str:pk>/', views.post_page, name='post_page'),
    path('post/like/<str:pk>/', views.like_post, name='like-post'),
    path('comment/like/<str:pk>/', views.like_comment, name='like-comment'),
    path('reply/like/<str:pk>/', views.like_reply, name='like-reply'),
    path('category/<slug:tag>/', views.home, name="category"),
    path('commentsent/<str:pk>/', views.comment_sent, name="comment-sent"),
    path('reply-sent/<str:pk>/', views.reply_sent, name="reply-sent"),
    path('comment/delete/<str:pk>/', views.comment_delete, name="comment-delete"),
    path('reply/delete/<str:pk>/', views.reply_delete, name="reply-delete"),
]

 