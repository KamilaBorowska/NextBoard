from django.views import generic

from forum.models import Forum

class ForumView(generic.ListView):
    model = Forum
