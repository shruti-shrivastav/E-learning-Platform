# teacher/forms.py

from django import forms
from .models import TeacherProfile

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['bio', 'specialization', 'profile_picture']
