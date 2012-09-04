from django.conf.urls import patterns, include, url
from django.views.generic import ListView

urlpatterns = patterns('',
        (r'^$', 'blog.views.get_entries'),
        (r'(?P<page>\d{1,2})/$', 'blog.views.get_entries'),
        (r'article/(?P<e_id>\d{1,3})$', 'blog.views.view_entry'),
        )
