from django import forms 
from courses.models import Course

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset = Course.objects.all(),
        widget= forms.HiddenInput
    )
    
    # def __int__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['course'].quertset = Course.objects.all()
    