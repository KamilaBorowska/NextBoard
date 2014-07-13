from django.views import generic

from forum.models import Forum, Thread

class ForumView(generic.ListView):
    model = Forum

class ThreadView(generic.ListView):
    model = Thread
