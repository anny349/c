from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .permissions import IsPostAuthor


# ===========================
# User Setup & Authentication
# ===========================

# Ensure user exists before creating
user, created = User.objects.get_or_create(username="new_user", defaults={"password": "secure_pass123"})
if created:
    print("User created:", user.username)
else:
    print("User already exists:", user.username)

# Authenticate user
user = authenticate(username="new_user", password="secure_pass123")
if user:
    print("Authentication successful!")
else:
    print("Invalid credentials. Ensure password is correct.")

# Create Admin Group if it doesn’t exist
admin_group, _ = Group.objects.get_or_create(name="Admin")

# Fetch or create admin user
admin_user, created = User.objects.get_or_create(username="admin_user")
if created:
    admin_user.set_password("adminpass")  # Hash the password properly
    admin_user.save()  # Save the user with the hashed password

# Assign the user to the Admin group
admin_user.groups.add(admin_group)


# ===================
# Function-Based APIs
# ===================

def get_users(request):
    """Retrieve all users."""
    try:
        users = list(User.objects.values('id', 'username', 'email', 'created_at'))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def create_user(request):
    """Create a new user."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create(username=data['username'], email=data['email'])
            return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def get_posts(request):
    """Retrieve all posts."""
    try:
        posts = list(Post.objects.values('id', 'content', 'author', 'created_at'))
        return JsonResponse(posts, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def create_post(request):
    """Create a new post."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            author = User.objects.get(id=data['author'])
            post = Post.objects.create(content=data['content'], author=author)
            return JsonResponse({'id': post.id, 'message': 'Post created successfully'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def get_comments(request):
    """Retrieve all comments."""
    try:
        comments = list(Comment.objects.values('id', 'text', 'author', 'post', 'created_at'))
        return JsonResponse(comments, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def create_comment(request):
    """Create a new comment."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            author = User.objects.get(id=data['author'])
            post = Post.objects.get(id=data['post'])
            comment = Comment.objects.create(text=data['text'], author=author, post=post)
            return JsonResponse({'id': comment.id, 'message': 'Comment created successfully'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# ===================
# Class-Based APIs
# ===================

class UserListCreate(APIView):
    """List all users or create a new user."""
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListCreate(APIView):
    """List all posts or create a new post."""
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreate(APIView):
    """List all comments or create a new comment."""
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """Retrieve a single post with authentication and author permissions."""
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)
        return Response({"content": post.content})


class ProtectedView(APIView):
    """Example of an authenticated view."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated!"})


# ===================
# Debugging
# ===================

# Create a test user with hashed password
test_user = User.objects.create_user(username="new_user", password="secure_pass123")
print(test_user.password)  # Outputs a hashed password
