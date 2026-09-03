from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Course, Module, Content, Subject
from django.db.models import Count
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from .forms import form
from django.apps import apps
from django.forms import modelform_factory
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from students.forms import CourseEnrollForm
from django.core.cache import cache

# Create your views here.
class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner = self.request.user)
class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('course:manage_course_list')
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'
    
class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'
    
class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'
    
class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'
    
class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'

#For Module
class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None
    def get_formset(self, data = None):
        return form(data = data, instance = self.course)
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, pk = pk, owner = self.request.user)
        return super().dispatch(request, pk)
    def post(self, request, *args, **kargs):
        form = self.get_formset(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('course:manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': form})
    def get(self, request, *args, **wargs):
        form = self.get_formset()
        return self.render_to_response(
            {'course': self.course, 'formset': form}
        )
        
#For Content
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'
    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(
                app_label='courses', model_name=model_name
            )
    def get_form(self, model, *args, **kwargs):
        form = modelform_factory(
            model, exclude= ['owner', 'order', 'created', 'updated']
        )
        return form(*args, **kwargs)
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(
            Module, id = module_id, course__owner = request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id = id, owner = request.user
            )
        return super().dispatch(request, module_id, model_name, id)
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, data = request.POST, instance = self.obj, files = request.FILES )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module = self.module, item = obj)
                return redirect('course:module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance = self.obj)
        return self.render_to_response({'form': form, 'object': object})
    
class ContentDeleteView(View):
    def post(self, request, pk):
        content = get_object_or_404(
            Content, id = pk, module__course__owner = request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('course:module_content_list', module.id )
    
class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'
    def get(self, request, module_id):
        module = get_object_or_404(
            Module, id = module_id, course__owner = request.user
        )
        return self.render_to_response({'module': module})

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id = id, course__owner = request.user).update(order = order)
        return self.render_json_response({'saved': 'OK'})
            
class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id = id, module__course__owner = request.user).update(order = order)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
    model = Subject
    template_name = 'courses/course/list.html'
    def get(self, request, subject = None):
        
        subjects = cache.get('all_subjects')
        
        if not subjects:
            subjects = Subject.objects.annotate(
                total_courses = Count('courses')
            )
            cache.set('all_subjects', subjects)
            
        all_courses = Course.objects.annotate(
            total_modules = Count('modules')
        )
        
        if subject:
            subject = get_object_or_404(
                Subject, slug = subject
            )
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject = subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
            
        return self.render_to_response({"subjects": subjects, "subject": subject, "courses": courses })

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object.id })
        return context





