from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string

# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    class Meta:
        ordering = ['title']
    def __str__(self):
        return self.title
class Course(models.Model):
    owner = models.ForeignKey( User, on_delete=models.CASCADE, related_name='courses_created')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    
    
    class Meta:
        ordering = ['-created']
    def __str__(self):        return self.title
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(for_fields = ['course'], blank = True, null = True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title
class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='contents')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model_in': ('text', 'video', 'image', 'file')})
    objects_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'objects_id')
    order = OrderField(for_fields = ['module'], blank = True, null = True)
    
    class Meta:
        ordering = ['order']
    
#Abstract Class or Model
class Itembase(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_related')
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    def __str__(self):
        return self.title
    def render(self):
        #the item object becomes self argument
        return render_to_string(f'courses/content/{self._meta.model_name}.html', {'item': self})
#Child Model
class Text(Itembase):
    content = models.TextField()
class File(Itembase):
    file = models.FileField(upload_to = 'files', blank=True)
class Image(Itembase):
    image = models.ImageField(upload_to = 'images', blank=True)
class Video(Itembase):
    url = models.URLField()
    