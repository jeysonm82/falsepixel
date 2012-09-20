from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from django.views.generic import TemplateView
urlpatterns = patterns('',
        (r'^$', 'blog.views.get_entries'),
        (r'(?P<page>\d{1,2})/$', 'blog.views.get_entries'),
        (r'article/(?P<e_id>\d{1,3})$', 'blog.views.view_entry'),
        (r'captcha/$', 'blog.views.serve_captcha'),
        (r'confirmation/$', 'blog.views.login_conf'),
        (r'logout/$', 'blog.views.logout_view'),
        (r'about/$', TemplateView.as_view(template_name='about.htm')), )
