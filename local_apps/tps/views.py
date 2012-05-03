from local_apps.tps.models import TPForm, TrabajoPractico, AlumnoForm, ValorControl, ValorControlForm,\
    validar_legajo
from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import re
from django.db.models.aggregates import Count
from django.conf import settings

#def login(request, next="/facultad/principal"):
#    return render_to_response('registration/login.html',
#                              {'next': next},
#                               context_instance=RequestContext(request))

@login_required
def index(request):
    if not request.user.has_perm('auth.change_user'):
        return HttpResponseForbidden()
    listaAlumnos = User.objects.filter(groups__name__contains='alumnos', is_active='True').order_by('-first_name')[:5]
    listaTPs = TrabajoPractico.objects.all().order_by('codigo', 'tema').annotate(dcount=Count('codigo'))
    t = loader.get_template('tps/index.html')
    c = Context ({
                  'listaAlumnos':listaAlumnos,
                  'listaTPs':listaTPs,
                  'result': validar_legajo('E-1009/0'),
    })
    return HttpResponse(t.render(c))

def error(request):
    t = loader.get_template('404.html')
    c = Context ({
                  'listaAlumnos':'',
    })
    return HttpResponse(t.render(c))

@login_required
def trabajosPracticos(request, tp_codigo, tp_tema):
    try:
        tp = TrabajoPractico.objects.get(codigo=tp_codigo, tema=tp_tema)
        form = TPForm(instance=tp)
        form.fields['codigo'].widget.attrs['readonly'] = 'True'
        form.fields['tema'].widget.attrs['readonly'] = 'True'
    except TrabajoPractico.DoesNotExist:
        raise Http404
    try:
        valoresCtrl = ValorControl.objects.filter(trabajoPractico=tp)
        #valCtrlForm = ValorControlForm(instance=valCtrl)
    except ValorControl.DoesNotExist:
        #valCtrlForm = ValorControlForm(instance=ValorControl())
        valoresCtrl = [ValorControl(),]
    return render_to_response('tps/forms.html',
                              {'formTP': form,
                               'codigoTP': str(tp.codigo) + '_' + tp.tema,
                               #'valCtrlForm': valCtrlForm,
                               'valoresCtrl': valoresCtrl,},
                              context_instance=RequestContext(request))

@login_required
def alumnos(request, legajo_id):
    try:
        alumno = User.objects.get(username=legajo_id)
        form = AlumnoForm(instance=alumno)
        form.fields['username'].widget.attrs['readonly'] = 'True'
    except User.DoesNotExist:
        raise Http404
    return render_to_response('tps/alumnos.html',
                              {'alumno': alumno,
                               'formAlumno': form,
                               'nroLegajoAsignacion': re.sub('^\w-{0,1}\d{3}|\/{0,1}\d{1}$', '', alumno.username),
                               #'cantTPAsignados':alumno.tpsAsignados.count
                               },
                               context_instance=RequestContext(request))

@login_required
def valorControl(request, tp_codigo, tp_tema, id_ValCtrl):
    try:
        valCtrl = ValorControl.objects.get(pk=id_ValCtrl)
        form = ValorControlForm(instance=valCtrl)
    except ValorControl.DoesNotExist:
        raise Http404
    return render_to_response('tps/forms.html',
                              {'formValCtrl': form,
                               },
                              context_instance=RequestContext(request))

@login_required
def asignarTP(request, legajo_id):
    alumno = User.objects.get(username=legajo_id)
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
        return HttpResponseRedirect(settings.FACULTAD_PRINCIPAL_PAGE)
    return HttpResponseRedirect('/facultad/alumno/'+alumno.nroLegajo)
    
@login_required
def agregarTP(request):
    if request.method == 'POST':
        try:
            tp = TrabajoPractico.objects.get(codigo = request.POST['codigo'], tema=request.POST['tema'])
        except TrabajoPractico.DoesNotExist:
            tp = TrabajoPractico()
        form = TPForm(request.POST, instance=tp)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(settings.FACULTAD_PRINCIPAL_PAGE)
    else:
        form = TPForm()
    return render_to_response('tps/forms.html',
                              {'formTP': form,},
                              context_instance=RequestContext(request))

@login_required
def agregarValorCtrl(request, tp_codigo, tp_tema):
    if request.method == 'POST':
        form = ValorControlForm(request.POST)
        if form.is_valid():
            valCtrl = form.save(commit=False)
            tp = TrabajoPractico.objects.get(codigo=tp_codigo, tema=tp_tema)
            valCtrl.trabajoPractico = tp
            valCtrl.save()
            return HttpResponseRedirect('/facultad/tps/'+tp_codigo+'_'+tp_tema)
    else:
        form = ValorControlForm()
    return render_to_response('tps/forms.html',
                              {'formValCtrl': form,},
                              context_instance=RequestContext(request))

@login_required
def agregarAlumno(request):
    if request.method == 'POST':
        #nroLegajoStr = formatLegajoToString(request.POST['nroLegajo'])
        #request.POST['nroLegajo'] = nroLegajoStr
        try:
            alumno = User.objects.get(username=request.POST['username'])
            alumnoInstance = alumno
        except User.DoesNotExist:
            alumnoInstance = User()
        
        form = AlumnoForm(request.POST, instance=alumnoInstance)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(settings.FACULTAD_PRINCIPAL_PAGE)
    else:
        form = AlumnoForm()
    return render_to_response('tps/forms.html',
                              {'formAlumno': form,},
                              context_instance=RequestContext(request))

def formatLegajoToString(legajo_id):
    legajo_id_str = re.sub('-|\/','',legajo_id)
    return legajo_id_str

#def formatLegajoFromString(legajo_id_str):
#    re.compile(pattern, flags)