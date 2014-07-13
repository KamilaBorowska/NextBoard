from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
    url(r'^$', views.ForumView.as_view(), name='forums'),
    url(r'^forums/(?P<forum_id>\d+)/$', views.ThreadView.as_view(), name='forum'),
    url(r'^thread/(?P<thread_id>\d+)/$', views.PostView.as_view(), name='thread'),
)
