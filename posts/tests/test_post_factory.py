from django.test import TestCase
from factories.post_factory import PostFactory
from posts.models import User

class PostFactoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")

    def test_post_creation(self):
        post = PostFactory.create_post(
            title="Test Post",
            post_type="text",
            content="This is a test post.",
            metadata={"category": "general"},
            author=self.user  # ✅ Pass the author to avoid IntegrityError
        )

        self.assertEqual(post.post_type, "text")
        self.assertEqual(post.content, "This is a test post.")
        self.assertEqual(post.author, self.user)
        print("✅ PostFactory test passed! Post created successfully.")
