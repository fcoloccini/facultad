from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to

urlpatterns = patterns ('',
    url(r'^principal', 'local_apps.tps.views.index'),
    url(r'^alumno/(?P<legajo_id>\w\d{5})', 'local_apps.tps.views.alumnos'),
    url(r'^alumno/agregarAlumno', 'local_apps.tps.views.agregarAlumno'),
    url(r'^tps/$', redirect_to,{'url': '/accounts/login/'}),
    url(r'^tps/(?P<tp_codigo>\d+)_(?P<tp_tema>[A-Z])/agregarValCtrl', 'local_apps.tps.views.agregarValorCtrl'),
    url(r'^tps/(?P<tp_codigo>\d+)_(?P<tp_tema>[A-Z])/valCtrl/(?P<id_ValCtrl>\d+)', 'local_apps.tps.views.valorControl'),
    url(r'^tps/(?P<tp_codigo>\d+)_(?P<tp_tema>[A-Z])/', 'local_apps.tps.views.trabajosPracticos'),
    url(r'^tps/error', 'local_apps.tps.views.error'),
    url(r'^tps/agregarTP', 'local_apps.tps.views.agregarTP'),
    #url(r'^asignarTP/(?P<legajo_id>\w\d{5})', 'local_apps.tps.views.asignarTP'),
)