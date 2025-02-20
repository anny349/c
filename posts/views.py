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

from .models import Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .permissions import IsPostAuthor


# ===========================
# User Setup & Authentication
# ===========================

class UserSetupView(APIView):
    """Setup initial users and authentication"""

    def post(self, request):
        # Extract username and password from request data
        username = request.data.get("username", "new_user")
        password = request.data.get("password", "secure_pass123")

        # Ensure user exists before creating
        user, created = User.objects.get_or_create(username=username, defaults={"password": password})
        if created:
            user.set_password(password)  # Hash the password
            user.save()
            message = f"User created: {user.username}"
        else:
            message = f"User already exists: {user.username}"

        # Authenticate user
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user:
            auth_message = "Authentication successful!"
        else:
            auth_message = "Invalid credentials. Ensure password is correct."

        # Create Admin Group if it doesn’t exist
        admin_group, _ = Group.objects.get_or_create(name="Admin")

        # Fetch or create admin user
        admin_user, created = User.objects.get_or_create(
            username="admin_user",
            defaults={"email": "admin@example.com"}
        )

        if created:
            admin_user.set_password("yourpassword")
            admin_user.save()

        # Assign the user to the Admin group
        admin_user.groups.add(admin_group)

        return Response(
            {
                "message": message,
                "auth_message": auth_message,
                "admin_message": f"Admin user {'created' if created else 'already exists'}",
            },
            status=status.HTTP_200_OK
        )


# ===================
# Function-Based APIs
# ===================

def get_users(request):
    """Retrieve all users."""
    try:
        users = list(User.objects.values('id', 'username', 'email'))
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



# LOGGING

from singletons.logger_singleton import LoggerSingleton


logger = LoggerSingleton().get_logger()
logger.info("API initialized successfully.")



# FACTORY


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from factories.post_factory import PostFactory


class CreatePostView(APIView):
    def post(self, request):
        data = request.data
        try:
            post = PostFactory.create_post(
                post_type=data['post_type'],
                title=data['title'],
                content=data.get('content', ''),
                metadata=data.get('metadata', {})
            )
            return Response({'message': 'Post created successfully!', 'post_id': post.id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
