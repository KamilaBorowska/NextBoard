from django.db import models
import django.contrib.auth.models as auth

class User(auth.User):
    """Model for representing users.

    It has few fields that aren't in the standard authentication user
    table, and are needed for the forum to work, like footers.
    """
    display_name = models.CharField(max_length=30, null=True)


class Thread(models.Model):
    """Model for representing threads."""
    title = models.TextField()
    views = models.PositiveIntegerField(default=0)
    sticky = models.BooleanField()
    closed = models.BooleanField()
