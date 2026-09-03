from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CourseEnrollForm
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('course:course_list')
    else:
        return redirect('student:student_registration')
    
@login_required
def request_teacher(request):
    return render(request, 'students/request_teacher.html')

class StudentRegistrationView(CreateView):
    template_name = 'students/student/registrations.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student:student_course_list')
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username = cd['username'],
            password = cd['password1'],
        )
        login(self.request, user)
        return result
    
class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm
    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)
    def form_invalid(self, form):
        print("=== FORM ERRORS ===")
        print(form.errors)
        print("=== SUBMITTED DATA ===")
        print(form.data)
        return redirect('course:course_list')
    def get_success_url(self):
        return reverse_lazy('student:student_course_detail', args=[self.course.id])

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in = [self.request.user]) #or you can use students = request.user and we use that because students is a many to many field
class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'
    def get_queryset(self):
        qs =  super().get_queryset()
        return qs.filter(students = self.request.user)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id = self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()[0]
        return context