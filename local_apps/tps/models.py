# -*- coding: utf-8 -*- 
from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import TextInput
# Create your models here.

class TrabajoPractico (models.Model):
    codigo = models.PositiveIntegerField('Código')
    titulo = models.CharField('Título', max_length=300)
    consigna = models.TextField()
    nrosLegajosAsignados = models.CommaSeparatedIntegerField('Nros Legajos Asignados', max_length=19)
    fechaInicio = models.DateField('Desde cuándo se activa')
    fechaFin = models.DateField('Último día en que está activo', null=True, blank=True)
    def __unicode__(self):
        return self.titulo
    
class Valor (models.Model):
    trabajoPractico = models.ForeignKey(TrabajoPractico)
    titulo = models.CharField('Título', max_length=500)
    valor = models.FloatField()

class Persona (models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    direccion = models.CharField('Dirección', max_length=200, null=True, blank=True)
    telefono = models.CharField('Teléfono', max_length=30, null=True, blank=True)
    pais = models.CharField('País', max_length=50, null=True, blank=True)
    provincia = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=200)
    def __unicode__(self):
        return self.nombre+" "+self.apellido

class Usuario (Persona):
    fechaAlta = models.DateField('Desde cuándo puede ingresar', auto_now_add=True)
    fechaBaja = models.DateField('Último día en que puede ingresar', null=True, blank=True)
    
class Alumno (Usuario):
    nroLegajo = models.CharField('Número de Legajo', max_length=10, unique=True)
    tpsAsignados = models.ManyToManyField(TrabajoPractico, blank=True, related_name='tpsAsignados')
    tpsValidados = models.ManyToManyField(TrabajoPractico, blank=True, related_name='tpsValidados')
    
#class TPForm (forms.Form):
#    codigo = forms.IntegerField(help_text="Este es el codigo unico del trabajo practico", widget=forms.TextInput({ "placeholder": "Codigo"}))
#    titulo = forms.CharField(max_length=300, widget=forms.TextInput({ "placeholder": "Titulo"}))
#    consigna = forms.CharField(widget=forms.Textarea({ "placeholder": "Consigna"}))
#    nrosLegajosAsignados = forms.CharField(label="Nros Legajos Asignados",
#                                           max_length=19,
#                                           widget=forms.TextInput({ "placeholder": "Ej: 1,2,6,9"}))
#    fechaInicio = forms.DateField(help_text="Fecha a partir de la cual el TP podra ser asignado",
#                                  label="Fecha inicio",
#                                  widget=forms.TextInput({ "placeholder": "Fecha inicio"}))
#    fechaFin = forms.DateField(required=False, label="Fecha fin", widget=forms.TextInput({ "placeholder": "Fecha fin"}))

class TPForm (ModelForm):
    class Meta:
        model = TrabajoPractico
        widgets = {
                   'nrosLegajosAsignados':TextInput(attrs={'required':'', 'pattern':'(\d,){0,9}(\d?)$'})}
    
#class AlumnoForm (forms.Form):
#    nroLegajo = forms.CharField(required=True, label = "Nro Legajo",max_length=10, widget=forms.TextInput({ "placeholder": "Ej: A-1234/1"}))
#    nombre = forms.CharField(max_length=200, widget=forms.TextInput({ "placeholder": "Nombre Alumno"}))
#    apellido = forms.CharField(max_length=200, widget=forms.TextInput({ "placeholder": "Apellido Alumno"}))
#    direccion = forms.CharField(max_length=200, required=False, widget=forms.TextInput({ "placeholder": "Direccion"}))
#    telefono = forms.CharField(max_length=30, required=False, widget=forms.TextInput({ "placeholder": "Telefono"}))
#    pais = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "Pais"}))
#    provincia = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "Provincia"}))
#    email = forms.EmailField(max_length=200, widget=forms.TextInput({ "placeholder": "Email"}))
#    fechaAlta = forms.DateField(label = "Fecha alta", widget=forms.TextInput({ "placeholder": "Fecha de alta"}))
#    fechaBaja = forms.DateField(label = "Fecha baja", required=False, widget=forms.TextInput({ "placeholder": "Fecha de baja"}))
class AlumnoForm (ModelForm):
    class Meta:
        model = Alumno
        exclude = ('tpsAsignados', 'tpsValidados',)
        widgets = {
                   'nroLegajo': TextInput(attrs={"placeholder": "Ej: A-1234/1 ó A12341"}),}#, "required":"", "pattern":"[A-Z]-\d{4}\/\d"}),}
        fields = ['nroLegajo','nombre','apellido','direccion','telefono','pais','provincia','email',]