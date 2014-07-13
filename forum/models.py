from django.db import models
import django.contrib.auth.models as auth

class User(auth.User):
    """Model for representing users.

    It has few fields that aren't in the standard authentication user
    table, and are needed for the forum to work, like footers.
    """
    display_name = models.CharField(max_length=30, null=True)
    footer = models.TextField(null=True)


class Thread(models.Model):
    """Model for representing threads."""
    title = models.CharField(max_length=100)
    views = models.PositiveIntegerField(default=0)
    sticky = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

class Post(models.Model):
    """Model for representing posts.

    Actual posts are stored in PostRevision, this only stores the
    thread number. The first created revision contains the author
    of post and date of its creation. The last revision contains actual
    text post.
    """
    thread = models.ForeignKey(Thread)

class PostRevision(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now=True)
    text = models.TextField()
