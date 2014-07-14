from django.views import generic

from forum.models import Category, Forum, Thread

class CategoryView(generic.ListView):
    model = Category

class ForumDetailView(generic.DetailView):
    model = Forum

class ThreadDetailView(generic.DetailView):
    model = Thread
