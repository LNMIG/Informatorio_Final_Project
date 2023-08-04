from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify


# Create your models here.

#MODELO ACERCA DE
class Acerca(models.Model):
    descripcion = models.CharField(max_length=450, verbose_name= 'Descripción')
    creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Acerca de'
        verbose_name_plural='Acerca de nosotros'
        ordering = ['-creacion']

    def __str__(self):
        return self.descripcion

#MODELO REDES SOCIALES
class Red(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Red Social')
    url = models.URLField(max_length=300, null=True, blank=True, verbose_name='Enlace')
    icono = models.CharField(max_length=150, null=True, blank=True, verbose_name='Icono')
    creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Red Social'
        verbose_name_plural = 'Redes Sociales'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

#MODELO CATEGORIA
class Categoria(models.Model):
    nombre = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    slug = models.SlugField(max_length=200)
    activo = models.BooleanField(default=True, verbose_name='Activo')
    creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Categoria, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre 

#MODELO ETIQUETA
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre 

#MODELO ARTICULOS
class Articulo(models.Model):
    titulo = models.CharField(max_length=250, unique=True, verbose_name='Título')
    slug = models.SlugField(max_length=250)
    bajada = models.CharField(max_length=150, verbose_name='Bajada')
    contenido = RichTextField(verbose_name='Contenido')
    imagen = models.ImageField(upload_to='blog/articulos/imagenes', null=True, blank=True, verbose_name='Imagen')
    publicado = models.BooleanField(default=True, verbose_name='Publicado')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_DEFAULT, default=1, related_name='get_articulos', verbose_name='Categoría')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='get_articulos', null=True, blank=True, verbose_name='Autor')
    etiquetas = models.ManyToManyField(Etiqueta, verbose_name='Etiquetas')
    creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        ordering = ['-creacion']

    def delete(self, using = None, keep_parents = False):
        self.imagen.delete(self.imagen.name)
        return super().delete()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(Articulo, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo

#MODELO COMENTARIOS
class Comentario(models.Model):
    contenido = models.TextField(verbose_name='Comentario')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='get_comentarios')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='get_comentarios')
    publicado = models.BooleanField(default=True, verbose_name='Publicado')
    creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['-creacion']

    def __str__(self):
        return self.contenido
