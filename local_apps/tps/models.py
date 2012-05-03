# -*- coding: utf-8 -*- 
from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import TextInput, Textarea
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django import forms

# Modelos #
class TrabajoPractico (models.Model):
    titulo = models.CharField('Título', max_length=300)
    codigo = models.PositiveIntegerField('Número TP')
    tema = models.CharField(max_length=5)
    consigna = models.TextField()
    nrosLegajosAsignados = models.CommaSeparatedIntegerField('Nros Legajos Asignados', max_length=19)
    fechaInicio = models.DateField('Desde cuándo se activa', null=True, blank=True)
    fechaFin = models.DateField('Último día en que está activo', null=True, blank=True)
    class Meta:
        unique_together = ("codigo", "tema")
    def __unicode__(self):
        return self.titulo
    
class ValorControl (models.Model):
    trabajoPractico = models.ForeignKey(TrabajoPractico)
    titulo = models.CharField('Título', max_length=500)
    valor = models.FloatField()
    unidad = models.CharField(max_length=10)
    ayuda = models.TextField('Forma de cálculo')

# Forms #
class TPForm (ModelForm):
    class Meta:
        model = TrabajoPractico
        widgets = {
                   'nrosLegajosAsignados':TextInput(attrs={'required':'', 'pattern':'(\d,){0,9}(\d?)$'}),
                   #'codigo':TextInput(attrs={'readonly':'True'}),
                   }
class ValorControlForm (ModelForm):
    #trabajoPractico = forms.Select
    #id = forms.CharField(widget=forms.HiddenInput(), required=False)
    #titulo = forms.CharField(max_length=500)
    #valor = forms.FloatField()
    #unidad = forms.CharField(max_length=10)
    #ayuda = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Se visualizará como ayuda'}), required=False)
    class Meta:
        model = ValorControl
        exclude = ('trabajoPractico')
    
    
class AlumnoForm (ModelForm):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'groups', 'user_permissions', 'password', 'last_login', 'date_joined',)
        #widgets = {
        #           'nroLegajo': TextInput(attrs={'placeholder': 'Ej: A-1234/1 ó A12341'}),}#, "required":"", "pattern":"[A-Z]-\d{4}\/\d"}),
        #           'last_login': TextInput(attrs={'readonly':'True'}),
        #           'date_joined': TextInput(attrs={'readonly':'True'}),
        #}
        #fields = ['nroLegajo','nombre','apellido','direccion','telefono','pais','provincia','email',]
        
# Validators
def validar_legajo(legajo):
    splitLeg = re.findall('\d', legajo)
    calculo = (int(splitLeg[3])*2 + int(splitLeg[2])*3 + int(splitLeg[1])*4 + int(splitLeg[0])*5) * 10
    residuo = calculo % 11
    nroControl = int(splitLeg[4])
    
    if residuo in range(1, 9) and residuo == nroControl:
        return True
    if residuo == 0 and nroControl == 1:
        return True
    if residuo == 10 and (nroControl == 0 or nroControl == 1):
        return True
    
    raise ValidationError(u'%s no es un legajo válido' % legajo)