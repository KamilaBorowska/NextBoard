from django.views import generic

from forum.models import Forum, Thread, Post

class ForumView(generic.ListView):
    model = Forum

class ForumDetailView(generic.DetailView):
    model = Forum

class PostView(generic.ListView):
    model = Post
