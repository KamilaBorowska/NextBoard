from django.test import TestCase
from forum.models import Forum, User, Thread, Post, PostRevision

class PostTestCase(TestCase):
    def setUp(self):
        """Prepare for testing posts."""
        user = User.objects.create(username='SampleGuy')
        author = User.objects.create(username='RelevantAuthor')

        forum = Forum.objects.create(title='Sample forum', description='Yes')
        thread = Thread.objects.create(forum=forum, title='This is it')
        post = Post.objects.create(thread=thread)

        PostRevision.objects.create(post=post, text='A', author=author)
        for content in ['B', 'C', 'D', 'E']:
            PostRevision.objects.create(post=post, text=content, author=user)

        # Create unrelated thread to find possible issues in query.
        unrelated_thread = Thread.objects.create(forum=forum, title='What?')
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

    def test_text(self):
        self.assertEqual(self.post.text(), 'E')

class ForumTestCase(TestCase):
    def setUp(self):
        """Prepare for testing forums."""
        create_forum = Forum.objects.create

        self.forums = forums = [
            create_forum(title='This forum.', description='Eh.'),
            create_forum(title='Creativity.', description='Is good.'),
            create_forum(title='Randomness.', description='Who cares?'),
            create_forum(title='Trash', description='Full of garbage.'),
        ]

        create_thread = Thread.objects.create

        self.threads = threads = [
            create_thread(forum=forums[0], title='A'),
            create_thread(forum=forums[0], title='B'),
            create_thread(forum=forums[2], title='C'),
        ]

        create_post = Post.objects.create

        posts = [
            create_post(thread=threads[0]),
            create_post(thread=threads[0]),
            create_post(thread=threads[1]),
            create_post(thread=threads[2]),
        ]

        user = User.objects.create()

        def create_revision(post, date, text):
            return PostRevision.objects.create(
                post=post,
                author=user,
                date_created=date,
                text=text
            )

        self.revisions = [
            create_revision(posts[0], '2000-01-01 00:00+00:00', 'D'),
            create_revision(posts[0], '2012-01-01 01:00+00:00', 'E'),
            create_revision(posts[1], '2001-02-02 02:00+00:00', 'F'),
            create_revision(posts[1], '2002-03-03 03:00+00:00', 'G'),
            create_revision(posts[1], '2003-04-04 04:00+00:00', 'H'),
            create_revision(posts[2], '2001-01-01 05:00+00:00', 'I'),
            create_revision(posts[3], '2000-12-31 06:00+00:00', 'J'),
        ]

    def test_last_post(self):
        """Last post should be last post, ignoring revisions."""

        self.assertEqual(self.forums[0].last_post().id, self.revisions[2].id)
        self.assertEqual(self.forums[1].last_post(), None)
        self.assertEqual(self.forums[2].last_post().id, self.revisions[6].id)
        self.assertEqual(self.forums[3].last_post(), None)

    def test_postcount(self):
        """Forums should have correct ammount of posts."""
        self.assertEqual(self.forums[0].postcount(), 3)
        self.assertEqual(self.forums[1].postcount(), 0)
        self.assertEqual(self.forums[2].postcount(), 1)
        self.assertEqual(self.forums[3].postcount(), 0)

    def test_thread_last_post(self):
        """Last post should be last post of given thread."""

        self.assertEqual(self.threads[0].last_post().id, self.revisions[2].id)
        self.assertEqual(self.threads[1].last_post().id, self.revisions[5].id)
        self.assertEqual(self.threads[2].last_post().id, self.revisions[6].id)

    def test_thread_replies(self):
        """Reply count should be number of post excluding first one."""

        self.assertEqual(self.threads[0].replies(), 1)
        self.assertEqual(self.threads[1].replies(), 0)
        self.assertEqual(self.threads[2].replies(), 0)
