from local_apps.tps.models import Alumno
from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    listaAlumnos = Alumno.objects.all().order_by('-nombre')[:5]
    t = loader.get_template('tps/index.html')
    c = Context ({
                  'listaAlumnos':listaAlumnos,
    })
    return HttpResponse(t.render(c))