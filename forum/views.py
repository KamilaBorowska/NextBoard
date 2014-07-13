from django.views import generic

from forum.models import Forum, Thread, Post

class ForumView(generic.ListView):
    model = Forum

class ThreadView(generic.ListView):
    model = Thread

class PostView(generic.ListView):
    model = Post
