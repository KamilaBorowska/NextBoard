from django.db import models

class Thread(models.Model):
    """Model for representing threads."""
    title = models.TextField()
    views = models.PositiveIntegerField(default=0)
    sticky = models.BooleanField()
    closed = models.BooleanField()
