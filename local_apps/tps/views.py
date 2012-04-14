from local_apps.tps.models import Alumno, TPForm, TrabajoPractico, AlumnoForm
from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import re

def login(request):
    return render_to_response('tps/login.html',
                               context_instance=RequestContext(request))

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

def trabajosPracticos(request, tp_codigo):
    try:
        tp = TrabajoPractico.objects.get(codigo=tp_codigo)
        form = TPForm(instance=tp)
    except TrabajoPractico.DoesNotExist:
        raise Http404
    return render_to_response('tps/forms.html',
                              {'formTP': form,},
                              context_instance=RequestContext(request))

def alumnos(request, legajo_id):
    try:
        alumno = Alumno.objects.get(nroLegajo=legajo_id)
        form = AlumnoForm(instance=alumno)
    except Alumno.DoesNotExist:
        raise Http404
    return render_to_response('tps/alumnos.html',
                              {'alumno': alumno,
                               'formAlumno': form,
                               'nroLegajoAsignacion': re.sub('^\w-{0,1}\d{3}|\/{0,1}\d{1}$', '', alumno.nroLegajo),
                               'cantTPAsignados':alumno.tpsAsignados.count},
                               context_instance=RequestContext(request))

def asignarTP(request, legajo_id):
    alumno = Alumno.objects.get(nroLegajo=legajo_id)
    nroLegajoAsignacion = re.sub('^\w-{0,1}\d{3}|\/{0,1}\d{1}$', '', alumno.nroLegajo)
    if alumno.tpsAsignados.count < '1':
        #tp = TrabajoPractico.objects.filter(nrosLegajosAsignados__contains=nroLegajoAsignacion)
        jump=False
        for tp in TrabajoPractico.objects.all(): #TODO mejorar esto, lo ideal es traer el tp filtradodesde el modelo
            nrosAsig = re.split(',', tp.nrosLegajosAsignados)
            for nro in nrosAsig:
                if nro == nroLegajoAsignacion:
                    alumno.tpsAsignados.add(tp)
                    alumno.save()
                    jump=True
                    break
            if jump:
                break
        return HttpResponseRedirect('/facultad/tps/principal')
    return HttpResponseRedirect('/facultad/tps/alumno/'+alumno.nroLegajo)
    
def agregarTP(request):
    if request.method == 'POST':
        form = TPForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/facultad/tps/principal')
    else:
        form = TPForm()
    return render_to_response('tps/forms.html',
                              {'formTP': form,},
                              context_instance=RequestContext(request))

def agregarAlumno(request):
    if request.method == 'POST':
        try:
            alumno = Alumno.objects.get(nroLegajo=request.POST['nroLegajo'])
            alumnoInstance = alumno
        except Alumno.DoesNotExist:
            alumnoInstance = Alumno()
        
        form = AlumnoForm(request.POST, instance=alumnoInstance)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/facultad/tps/principal')
    else:
        form = AlumnoForm()
    return render_to_response('tps/forms.html',
                              {'formAlumno': form,},
                              context_instance=RequestContext(request))

def validarLegajo(legajo_id):
    return False

def formatLegajoToString(legajo_id):
    legajo_id_str = re.sub('-|\/','',legajo_id)
    return legajo_id_str

#def formatLegajoFromString(legajo_id_str):
#    re.compile(pattern, flags)