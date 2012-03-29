from local_apps.tps.models import Alumno
from django.template import Context, loader
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def index(request):
    listaAlumnos = Alumno.objects.all().order_by('-nombre')[:5]
    t = loader.get_template('tps/index.html')
    c = Context ({
                  'listaAlumnos':listaAlumnos,
    })
    return HttpResponse(t.render(c))

def error(request):
    t = loader.get_template('404.html')
    c = Context ({
                  'listaAlumnos':'',
    })
    return HttpResponse(t.render(c))

def trabajosPracticos(request, legajo_id):
    try:
        alumno = Alumno.objects.get(nroLegajo=legajo_id)
    except Alumno.DoesNotExist:
        raise Http404
    return render_to_response('tps/trabajosPracticos.html',
                              {'alumno': alumno})
def nuevoTP(request):
    return render_to_response('tps/agregarTrabajosPracticos.html',
                              context_instance=RequestContext(request))
    