from django.test import TestCase
from forum.models import User, Thread, Post, PostRevision

class PostTestCase(TestCase):
    def setUp(self):
        """Prepare for testing posts."""
        user = User.objects.create(username='SampleGuy')
        author = User.objects.create(username='RelevantAuthor')

        thread = Thread.objects.create(title='This is it')
        post = Post.objects.create(thread=thread)

        PostRevision.objects.create(post=post, text='A', author=author)
        for content in ['B', 'C', 'D', 'E']:
            PostRevision.objects.create(post=post, text=content, author=user)

        # Create unrelated thread to find possible issues in query.
        unrelated_thread = Thread.objects.create(title='Unrelated thread')
        unrelated_post = Post.objects.create(thread=unrelated_thread)
        PostRevision.objects.create(post=unrelated_post, text='F', author=user)

        self.post = post
        self.author = author

    def test_first_revision(self):
        """First revision should be the initial revision."""
        self.assertEqual(self.post.first_revision().text, 'A')

    def test_last_revision(self):
        """Last revision should be the final revision."""
        self.assertEqual(self.post.last_revision().text, 'E')

    def test_author(self):
        self.assertEqual(self.post.author(), self.author)
