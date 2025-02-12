from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserSetupView, get_users, create_user, UserListCreate,
    PostListCreate, CommentListCreate, PostDetailView, ProtectedView
)

urlpatterns = [
    # User authentication & setup
    path('setup-user/', UserSetupView.as_view(), name='user-setup'),
    path('get-users/', get_users, name='get-users'),
    path('create-user/', create_user, name='create-user'),
    path('users/', UserListCreate.as_view(), name='user-list-create'),

    # Post and comment management
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    
    # Authentication & protected routes
    path('auth-token/', obtain_auth_token, name='auth-token'),
    path('protected/', ProtectedView.as_view(), name='protected-view'),
]
