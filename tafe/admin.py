from tafe.models import Student, Course, Subject, Enrolment, Grade, Attendance, SubjectResults
from django.contrib import admin
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget 
from django.forms.widgets import RadioSelect

class StudentAdminForm(ModelForm):
    class Meta:
        model = Student
        widgets = {
            'dob': SelectDateWidget(),
            'gender': RadioSelect(),
        }            

class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm

class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    prepopulated_fields = {'slug': ('name','year')}

class CourseAdmin(admin.ModelAdmin):
    model = Course
    prepopulated_fields = {'slug': ('name',)}

class AttendanceInline(admin.StackedInline):
    model = Attendance
    template = 'admin/collapsed_tabular_inline.html'
    
class SubjectResultsInline(admin.StackedInline):
    model = SubjectResults
    template = 'admin/collapsed_tabular_inline.html'

class GradeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('',{'fields':['student','subject','date_started','results','attendance']}),
    ]

class EnrolmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('',{'fields':['student','course','date_started','date_ended','mark']}),
    ]

admin.site.register(Attendance)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Enrolment, EnrolmentAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(SubjectResults)
