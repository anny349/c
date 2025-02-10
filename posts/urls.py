
# from django.urls import path
# from django.contrib import admin
# from . import views


# urlpatterns = [

#     path('users/', views.get_users, name='get_users'),
#     path('users/create/', views.create_user, name='create_user'),
#     path('posts/', views.get_posts, name='get_posts'),
#     path('posts/create/', views.create_post, name='create_post'),
# ]
# ###


# from django.urls import path
# from .views import UserListCreate, PostListCreate, CommentListCreate


# urlpatterns = [
#     path('users/', UserListCreate.as_view(), name='user-list-create'),
#     path('posts/', PostListCreate.as_view(), name='post-list-create'),
#     path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
# ]


from django.urls import path
from .views import (
    get_users, create_user, get_posts, create_post, get_comments, create_comment,  # Function-based views
    UserListCreate, PostListCreate, CommentListCreate  # Class-based views
)

urlpatterns = [
    
    path('users/', get_users, name='get_users'),
    path('users/create/', create_user, name='create_user'),
    path('posts/', get_posts, name='get_posts'),
    path('posts/create/', create_post, name='create_post'),
    path('comments/', get_comments, name='get_comments'),  
    path('comments/create/', create_comment, name='create_comment'),  
    
    path('users/list/', UserListCreate.as_view(), name='user-list-create'),
    path('posts/list/', PostListCreate.as_view(), name='post-list-create'),
    path('comments/list/', CommentListCreate.as_view(), name='comment-list-create'),
]