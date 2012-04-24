# -*- coding: utf-8 -*- 
from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import TextInput, Textarea
from django.contrib.auth.models import User, Group

# Modelos #
class TrabajoPractico (models.Model):
    titulo = models.CharField('Título', max_length=300)
    codigo = models.PositiveIntegerField('Número TP')
    tema = models.CharField(max_length=5)
    consigna = models.TextField()
    nrosLegajosAsignados = models.CommaSeparatedIntegerField('Nros Legajos Asignados', max_length=19)
    fechaInicio = models.DateField('Desde cuándo se activa')
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
    
#class Alumno (User):
#    nroLegajo = models.CharField('Número de Legajo', max_length=10, unique=True)
#    telefono = models.CharField('Teléfono', max_length=30, null=True, blank=True)
#    tpsAsignados = models.ManyToManyField(TrabajoPractico, blank=True, related_name='tpsAsignados')
#    tpsValidados = models.ManyToManyField(TrabajoPractico, blank=True, related_name='tpsValidados')

# Forms #
class TPForm (ModelForm):
    class Meta:
        model = TrabajoPractico
        widgets = {
                   'nrosLegajosAsignados':TextInput(attrs={'required':'', 'pattern':'(\d,){0,9}(\d?)$'}),
                   #'codigo':TextInput(attrs={'readonly':'True'}),
                   }
class ValorControlForm (ModelForm):
    class Meta:
        model = ValorControl
        widgets = {
                   'ayuda':Textarea(attrs={'placeholder':'Se visualizará como ayuda'}),
                   }
    
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