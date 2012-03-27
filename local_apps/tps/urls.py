from django.conf.urls.defaults import patterns, url

urlpatterns = patterns ('',
    url(r'^tps/$', 'local_apps.tps.views.index'),
    url(r'^tps/(?P<legajo_id>\d+)', 'local_apps.tps.views.trabajos'),
)