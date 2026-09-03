from django.contrib import admin
from .models import Subject, Course, Module, Text, Video, File, Image

# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'slug',
    ]
    prepopulated_fields = {
        'slug': ('title', )
    }
admin.site.register(Subject, SubjectAdmin)

class ModuleAdmin(admin.StackedInline):
    model = Module
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'subject',
        'created'
    ]
    list_filter = [
        'created', 
        'subject',
    ]
    search_fields = [
        'title', 
        'overview'
    ]
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = [ ModuleAdmin]
admin.site.register(Course, CourseAdmin)
admin.site.register(Text)
admin.site.register(Video)
admin.site.register(Image)
admin.site.register(File)