from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'facultad.views.home', name='home'),
    # url(r'^facultad/', include('facultad.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^facultad/', include('local_apps.tps.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('invitation.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
