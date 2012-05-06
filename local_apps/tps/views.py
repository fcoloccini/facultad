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
    #Muestra el index principal dependiendo si es profesor o alumno
    isProfesor = validateGroupProfesores(request.user)
    
    if isProfesor:
        listaAlumnos = User.objects.filter(groups__name__contains='alumnos', is_active='True').order_by('-first_name')[:5]
        listaTPs = TrabajoPractico.objects.all().order_by('codigo', 'tema').annotate(dcount=Count('codigo'))
        t = loader.get_template('tps/indexProfesores.html')
    else:
        #Si es alumno
        listaAlumnos = (User.objects.get(username=request.user.username),)
        nroLegajoAsignacion = getNroLegajoAsignacion(request.user.username)
        listaTPs = TrabajoPractico.objects.filter(nrosLegajosAsignados__contains=nroLegajoAsignacion).order_by('codigo', 'tema').annotate(dcount=Count('codigo'))
        t = loader.get_template('tps/indexAlumnos.html')
        
    c = Context ({
                  'user': request.user,
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

@login_required
def trabajosPracticos(request, tp_codigo, tp_tema):
    if validateGroupProfesores(request.user):
        try:
            tp = TrabajoPractico.objects.get(codigo=tp_codigo, tema=tp_tema)
            form = TPForm(instance=tp)
            form.fields['codigo'].widget.attrs['readonly'] = 'True'
            form.fields['tema'].widget.attrs['readonly'] = 'True'
        except TrabajoPractico.DoesNotExist:
            raise Http404
        try:
            valoresCtrl = ValorControl.objects.filter(trabajoPractico=tp)
        except ValorControl.DoesNotExist:
            valoresCtrl = [ValorControl(),]
        return render_to_response('tps/forms.html',
                                  {'formTP': form,
                                   'codigoTP': str(tp.codigo) + '_' + tp.tema,
                                   'valoresCtrl': valoresCtrl,},
                                  context_instance=RequestContext(request))
    else:
        try:
            tp = TrabajoPractico.objects.get(codigo=tp_codigo, tema=tp_tema)
        except TrabajoPractico.DoesNotExist:
            raise Http404
        try:
            valoresCtrl = ValorControl.objects.filter(trabajoPractico=tp)
        except ValorControl.DoesNotExist:
            valoresCtrl = [ValorControl(),]
        return render_to_response('tps/autoevaluacionValoresCtrl.html',
                                  {'user': request.user,
                                   'codigoTP': str(tp.codigo) + '_' + tp.tema,
                                   'tp': tp,
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
                               'nroLegajoAsignacion': getNroLegajoAsignacion(alumno.username),
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

def validarValoresControl(request, tp_codigo, tp_tema):
    if request.method == 'POST':
        try:
            tp = TrabajoPractico.objects.get(codigo=tp_codigo, tema=tp_tema)
            valoresCorrectos = ValorControl.objects.filter(trabajoPractico=tp)
            for valorCorrecto in valoresCorrectos:
                request.POST[valorCorrecto.id]
        except TrabajoPractico.DoesNotExist:
            raise Http404
    
#@login_required
#def asignarTP(request, legajo_id):
#    #Valida permisos
#    if not request.user.has_perms(['tps.change_trabajoPractico','auth.change_user']):
#        return HttpResponseForbidden()
#    
#    alumno = User.objects.get(username=legajo_id)
#    if alumno.tpsAsignados.count < '1':
#        #tp = TrabajoPractico.objects.filter(nrosLegajosAsignados__contains=nroLegajoAsignacion)
#        jump=False
#        for tp in TrabajoPractico.objects.all(): #TODO mejorar esto, lo ideal es traer el tp filtradodesde el modelo
#            nrosAsig = re.split(',', tp.nrosLegajosAsignados)
#            nroLegajoAsignacion = getNroLegajoAsignacion(alumno.username)
#            for nro in nrosAsig:
#                if nro == nroLegajoAsignacion:
#                    alumno.tpsAsignados.add(tp)
#                    alumno.save()
#                    jump=True
#                    break
#            if jump:
#                break
#        return HttpResponseRedirect(settings.FACULTAD_PRINCIPAL_PAGE)
#    return HttpResponseRedirect('/facultad/alumno/'+alumno.nroLegajo)
    
@login_required
def agregarTP(request):
    #Valida permisos
    if not request.user.has_perm('tps.change_trabajopractico'):
        return HttpResponseForbidden()
    
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
    #Valida permisos
    if not request.user.has_perms(['tps.change_trabajopractico','tps.change_valorcontrol']):
        return HttpResponseForbidden()
    
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
    #Valida permisos
    if not request.user.has_perm('auth.change_user'):
        return HttpResponseForbidden()
    
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

def getNroLegajoAsignacion(legajo):
    return re.sub('^\w-{0,1}\d{3}|\/{0,1}\d{1}$', '', legajo)

def validateGroupProfesores(user):
    isProfesor = False
    for group in user.groups.all():
        if group.name == 'profesores':
            isProfesor = True
            break
    return isProfesor
#def formatLegajoFromString(legajo_id_str):
#    re.compile(pattern, flags)