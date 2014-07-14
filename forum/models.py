from django.db import models
import django.contrib.auth.models as auth

class User(auth.User):
    """Model for representing users.

    It has few fields that aren't in the standard authentication user
    table, and are needed for the forum to work, like footers.
    """
    display_name = models.CharField(max_length=30, null=True)
    footer = models.TextField(null=True)

    def __str__(self):
        """Show display name or user name."""
        return self.display_name or self.username

class Forum(models.Model):
    """Model for representing forums."""
    title = models.TextField()
    description = models.TextField()

    def __str__(self):
        """Show forum title."""
        return self.title

    def postcount(self):
        """Show forum postcount."""
        return Post.objects.filter(thread__forum=self).count()

    def last_post(self):
        """Show last post in the forum."""
        result = PostRevision.objects.raw('''
            SELECT postrevision.id, post_id, author_id, date_created, text
                FROM forum_post AS post
                JOIN forum_postrevision AS postrevision
                    ON postrevision.id = (SELECT id
                        FROM forum_postrevision
                        WHERE post_id = post.id
                        ORDER BY date_created
                        LIMIT 1
                    )
                JOIN forum_thread AS thread
                    ON thread.id = thread_id
                WHERE forum_id = %s
                ORDER BY date_created
                LIMIT 1
        ''', [self.id])

        try:
            return result[0]
        except IndexError:
            return None

class Thread(models.Model):
    """Model for representing threads."""
    forum = models.ForeignKey(Forum)
    title = models.CharField(max_length=100)
    views = models.PositiveIntegerField(default=0)
    sticky = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    def __str__(self):
        """Show thread title."""
        return self.title

class Post(models.Model):
    """Model for representing posts.

    Actual posts are stored in PostRevision, this only stores the
    thread number. The first created revision contains the author
    of post and date of its creation. The last revision contains actual
    text post.
    """
    thread = models.ForeignKey(Thread)

    def first_revision(self):
        """Get first revision.

        The first revision is important for things like post author.
        """
        return self.postrevision_set.first()

    def last_revision(self):
        """Get last revision.

        The last revision contains most current post contents.
        """
        return self.postrevision_set.last()

    def author(self):
        """Get author.

        This usually shows along with the post.
        """
        return self.first_revision().author

    def text(self):
        """Get post contents."""
        return self.last_revision().text

class PostRevision(models.Model):
    """Model for representing post revisions.

    The first revision for given post contains its author and date to
    show to the user. The last revision shows the date it was created
    on.
    """
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ['date_created']
