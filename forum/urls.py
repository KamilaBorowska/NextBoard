from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
    url(r'^$', views.ForumView.as_view(), name='forums'),
    url(r'^forum/(?P<pk>\d+)/$', views.ForumDetailView.as_view(), name='forum'),
    url(r'^thread/(?P<pk>\d+)/$', views.ThreadDetailView.as_view(), name='thread'),
)
