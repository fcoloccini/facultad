from django.db import models
from django import forms
# Create your models here.

class TrabajoPractico (models.Model):
    codigo = models.PositiveIntegerField()
    titulo = models.CharField(max_length=300)
    consigna = models.TextField()
    fechaInicio = models.DateField('fecha desde la que el tp se activa')
    fechaFin = models.DateField(name='fecha hasta la que el tp esta activo', null=True, blank=True)
    def __unicode__(self):
        return self.titulo
    
class Valor (models.Model):
    trabajoPractico = models.ForeignKey(TrabajoPractico)
    titulo = models.CharField(max_length=500)
    valor = models.FloatField()

class Persona (models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    dieccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=30)
    pais = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    def __unicode__(self):
        return self.nombre+" "+self.apellido

class Usuario (Persona):
    fechaAlta = models.DateField('fecha desde la que el usuario puede ingresar')
    fechaBaja = models.DateField('fecha hasta la que el usuario puede ingresar')
    
class Alumno (Usuario):
    nroLegajo = models.CharField(max_length=10)
    tpsAsignados = models.ManyToManyField(TrabajoPractico, blank=True, related_name='tpsAsignados')
    tpsValidados = models.ManyToManyField(TrabajoPractico, blank=True, related_name='tpsValidados')
    
class TPForm (forms.Form):
    codigo = forms.IntegerField(help_text="Este es el codigo unico del trabajo practico", widget=forms.TextInput({ "placeholder": "Codigo"}))
    titulo = forms.CharField(max_length=300, widget=forms.TextInput({ "placeholder": "Titulo"}))
    consigna = forms.CharField(widget=forms.TextInput({ "placeholder": "Consigna"}))
    fechaInicio = forms.DateField(help_text="Fecha a partir de la cual el TP podra ser asignado",
                                  label="Fecha inicio",
                                  widget=forms.TextInput({ "placeholder": "Fecha inicio"}))
    fechaFin = forms.DateField(required=False, label="Fecha fin", widget=forms.TextInput({ "placeholder": "Fecha fin"}))

class AlumnoForm (forms.Form):
    nroLegajo = forms.CharField(required=True, label = "Nro Legajo",max_length=10, widget=forms.TextInput({ "placeholder": "Nro de Legajo"}))
    nombre = forms.CharField(max_length=200, widget=forms.TextInput({ "placeholder": "Nombre Alumno"}))
    apellido = forms.CharField(max_length=200, widget=forms.TextInput({ "placeholder": "Apellido Alumno"}))
    direccion = forms.CharField(max_length=200, required=False, widget=forms.TextInput({ "placeholder": "Direccion"}))
    telefono = forms.CharField(max_length=30, required=False, widget=forms.TextInput({ "placeholder": "Telefono"}))
    pais = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "Pais"}))
    provincia = forms.CharField(max_length=50, required=False, widget=forms.TextInput({ "placeholder": "Provincia"}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput({ "placeholder": "Email"}))
    fechaAlta = forms.DateField(label = "Fecha alta", widget=forms.TextInput({ "placeholder": "Fecha de alta"}))
    fechaBaja = forms.DateField(label = "Fecha baja", required=False, widget=forms.TextInput({ "placeholder": "Fecha de baja"}))
    