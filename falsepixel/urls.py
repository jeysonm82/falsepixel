from django.conf.urls import patterns, include, url
from blog.views import test, contact, index, log_error
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'falsepixel.views.home', name='home'),
    # url(r'^falsepixel/', include('falsepixel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^test/', test),
     url(r'^error/', log_error),
     url(r'^$', index),
     url(r'^blog/', include('blog.urls')),
     url(r'^contact/', contact),
     url(r'', include('social_auth.urls')),

)
