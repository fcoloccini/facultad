from django.conf.urls.defaults import patterns, url

urlpatterns = patterns ('',
    url(r'^tps/$', 'local_apps.tps.views.index'),
    url(r'^tps/(?P<legajo_id>\w\d{5})', 'local_apps.tps.views.trabajosPracticos'),
    url(r'^tps/error', 'local_apps.tps.views.error'),
    url(r'^tps/asignarTP/(?P<legajo_id>\w\d{5})', 'local_apps.tps.views.asignarTP'),
    url(r'^tps/agregarTP', 'local_apps.tps.views.agregarTP'),
    url(r'^tps/agregarAlumno', 'local_apps.tps.views.agregarAlumno'),
)