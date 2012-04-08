from local_apps.tps.models import Alumno, TPForm, TrabajoPractico, AlumnoForm
from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def index(request):
    listaAlumnos = Alumno.objects.all().order_by('-nombre')[:5]
    listaTPs = TrabajoPractico.objects.all().order_by('-codigo')[:5]
    t = loader.get_template('tps/index.html')
    c = Context ({
                  'listaAlumnos':listaAlumnos,
                  'listaTPs':listaTPs,
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

def agregarTP(request):
    if request.method == 'POST':
        form = TPForm(request.POST)
        if form.is_valid():
            tp = TrabajoPractico()
            tp.codigo = form.cleaned_data['codigo']
            tp.titulo = form.cleaned_data['titulo']
            tp.consigna = form.cleaned_data['consigna']
            tp.fechaInicio = form.cleaned_data['fechaInicio']
            tp.fechaFin = form.cleaned_data['fechaFin']
            tp.save()
            return HttpResponseRedirect('./')
    else:
        form = TPForm()
    return render_to_response('tps/forms.html',
                              {'formTP': form,},
                              context_instance=RequestContext(request))

def agregarAlumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = Alumno()
            alumno.nroLegajo = form.cleaned_data['nroLegajo']
            alumno.nombre = form.cleaned_data['nombre']
            alumno.apellido = form.cleaned_data['apellido']
            alumno.dieccion = form.cleaned_data['dieccion']
            alumno.email = form.cleaned_data['email']
            alumno.fechaAlta = form.cleaned_data['fechaAlta']
            alumno.fechaBaja = form.cleaned_data['fechaBaja']
            alumno.pais = form.cleaned_data['pais']
            alumno.provincia = form.cleaned_data['provincia']
            alumno.telefono = form.cleaned_data['telefono']
            alumno.save()
            return HttpResponseRedirect('./')
    else:
        form = AlumnoForm()
    return render_to_response('tps/forms.html',
                              {'formAlumno': form,},
                              context_instance=RequestContext(request))