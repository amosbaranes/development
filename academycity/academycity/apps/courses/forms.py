from django import forms
from django.forms.models import inlineformset_factory
from .models import (CourseSchedule, Assignment)

# ModuleFormSet = inlineformset_factory(Course,
#                                       CourseSchedule,
#                                       fields=['owner', 'course', 'instructors', 'start_date',
#                                               'end_date', 'active', 'name', 'price'],
#                                       extra=0,
#                                       can_delete=True)
#
#
# class CourseScheduleForm(forms.ModelForm):
#     class Meta:
#         model = CourseSchedule
#         fields = ('course', 'name', 'owner', 'instructors', 'start_date', 'end_date', 'price', 'active')

CourseScheduleFormSet = inlineformset_factory(CourseSchedule,
                                              Assignment,
                                              fields=['sub_section', 'course_schedule', 'assignment_type',
                                                      'period_start', 'period_end'],
                                              extra=0,
                                              can_delete=True)


class CourseScheduleEmailForm(forms.Form):
    # name = forms.CharField(max_length=25)
    # email = forms.EmailField()
    subject = forms.CharField(max_length=128)
    message = forms.CharField(required=False, widget=forms.Textarea)
    file = forms.FileField()
    slug = forms.CharField(widget=forms.HiddenInput(), required=False, initial=False)

