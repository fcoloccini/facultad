from django.db import models

# Create your models here.

class TrabajoPractico (models.Model):
    codigo = models.PositiveIntegerField()
    titulo = models.CharField(max_length=300)
    consigna = models.TextField()
    fechaInicio = models.DateField('fecha desde la que el tp se activa')
    fechaFin = models.DateField('fecha hasta la que el tp esta activo')
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
    tpsAsignados = models.ManyToManyField(TrabajoPractico)
    tpsValidados = models.ManyToManyField(TrabajoPractico)
