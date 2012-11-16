from tafe.models import Student, Course, Subject, Enrolment, Grade, StaffAttendance, StudentAttendance, Result, Session, Timetable, Applicant, Staff, Credential, Assessment
from django.contrib import admin
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget 
from django.forms.widgets import RadioSelect
import datetime

today = datetime.date.today()
this_year = datetime.date.today().year
BIRTH_YEARS = range(this_year-51, this_year-15)

class ApplicantInline(admin.TabularInline):
    model = Applicant
    extra = 1

class AssessmentInline(admin.TabularInline):
    model = Assessment 

class CourseInline(admin.TabularInline):
    model = Course

class CredentialInline(admin.TabularInline):
    model = Staff.credential.through

class EnrolmentInline(admin.TabularInline):
    model = Enrolment 
    extra = 1    

class GradeInline(admin.TabularInline):
    model = Grade
    fields = ('student','date_started','results')

class ResultInline(admin.StackedInline):
    model = Result
    template = 'admin/collapsed_tabular_inline.html'

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    fields = ('date', 'session_number','subject','timetable')
    template = 'admin/collapsed_tabular_inline.html'

class StaffAttendanceInline(admin.TabularInline):
    model = StaffAttendance
    exclude = ('slug',)
    extra = 1
    fields = ('staff_member','reason','absent')
    template = 'admin/collapsed_tabular_inline.html'

class StudentAttendanceInline(admin.TabularInline):
    model = StudentAttendance
    fields = ('student','reason','absent')
    exclude = ('slug',)
    template = 'admin/collapsed_tabular_inline.html'

class StudentInline(admin.StackedInline):
    model = Student

class StaffInline(admin.StackedInline):
    model = Staff

class SubjectInline(admin.StackedInline):
    model = Subject

class ApplicantAdminForm(ModelForm):
    class Meta:
        model = Applicant 
        widgets = {
            'dob': SelectDateWidget(years=BIRTH_YEARS),
            'gender': RadioSelect(),
        }            

class ApplicantAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Bio', {'fields':(('first_name','surname'),('dob','gender', 'island'))}),
        ('Contact Information', { 'fields':(('phone','email'),)}),
        ('Other Information', { 'fields':(('disability','disability_description'), 'education_level')}),
        ('Course Applied For', { 'fields':(('applied_for', 'date_of_application', 'short_listed'),)}),
        ('Test Results', {'fields':(('test_ma','test_eng'),)}),
        ('Short Listing', {'fields':(('short_listed','test_ap'),)}),
        ('Ranking, Eligibility and Success', {'fields':(('ranking','eligibility','successful'),)}),
        ('Offer details', {'fields':(('date_offer_sent','date_offer_accepted'),)}),
        ('Admin (non editable)', {'fields':(('added', 'updated','last_change_by','penultimate_change_by'),)}),
    )
    form = ApplicantAdminForm
    list_display = ('__unicode__', 'gender', 'disability', 'applied_for', 'eligibility', 'successful')
    list_filter = ('gender', 'disability', 'applied_for', 'eligibility', 'successful')
    readonly_fields = ('added', 'updated','last_change_by','penultimate_change_by')
    actions = ['make_student', 'mark_unsuccessful']

    def mark_unsuccessful(self, request, queryset):
        '''Marks a group of applicants as unsuccessful'''
        rows_updated = 0
        for applicant in queryset:
            applicant.successful = 0 #0 == FALSE
            applicant.save()
            rows_updated += 1

        if rows_updated == 1:
            message_bit = "1 applicant was"
        else:
            message_bit = "%s applicants were" % rows_updated
        self.message_user(request, "%s marked unsuccessful." % message_bit)

    def make_student(self, request, queryset):
        '''Creates a convert to student option for applicants on the admin screen'''
        rows_updated = 0
        for applicant in queryset:
            applicant.convert_to_student()
            rows_updated += 1

        if rows_updated == 1:
            message_bit = "1 applicant was"
        else:
            message_bit = "%s applicants were" % rows_updated
        self.message_user(request, "%s successfuly converted to students." % message_bit)
    
    def save_model(self, request, obj, form, change): 
        try:
            obj.last_change_by
        except:
            pass
        else:
            obj.penultimate_change_by = obj.last_change_by 
        obj.last_change_by = request.user 
        obj.save()

class ApplicantSuccess(admin.TabularInline):
    model = Student
    fields = ('__unicode__','successful')

class AssessmentAdmin(admin.ModelAdmin):
    model = Assessment
    fields = ('name','slug','subject','date_given','date_due')
    list_display = ('name','subject','date_given','date_due')
    list_filter = ('name','subject')
    prepopulated_fields = {'slug': ('name',)}

class StudentAttendanceAdmin(admin.ModelAdmin):
    model = StudentAttendance
    list_display = ('student','session','reason','absent')
    list_filter = ('reason','absent')
    
    def save_model(self, request, obj, form, change): 
        try:
            obj.last_change_by
        except:
            pass
        else:
            obj.penultimate_change_by = obj.last_change_by 
        obj.last_change_by = request.user 
        obj.save()

class CourseAdmin(admin.ModelAdmin):
    inlines = (EnrolmentInline,
               ApplicantInline,
        )
    filter_horizontal = ('subjects',)
    fieldsets = (
        ('', { 'fields':(('name','year', 'slug'),)}),
        ('Subjects', { 'fields':('subjects',)}),
    )
    list_display = ('name', 'count_students', 'count_males', 'count_females', 'subjects_available')
    model = Course 
    prepopulated_fields = {'slug': ('name',)}

    def save_formset(self, request, form, formset, change): 
        if formset.model == Enrolment:
            instances = formset.save(commit=False)
            for instance in instances:
                try:
                    instance.last_change_by
                except:
                    pass
                else:   
                    instance.penultimate_change_by = instance.last_change_by
                instance.last_change_by = request.user
                instance.save()
        else:
            formset.save()

class CredentialAdmin(admin.ModelAdmin):
    fieldsets = [
        ('',{'fields':[('name','year'),('institution','aqf_level'),'type']}),
    ]

    def save_model(self, request, obj, form, change): 
        try:
            obj.last_change_by
        except:
            pass
        else:
            obj.penultimate_change_by = obj.last_change_by 
        obj.last_change_by = request.user 
        obj.save()

class EnrolmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('',{'fields':['student','course','date_started','date_ended','mark']}),
        ('Admin (non editable)', {'fields':(('last_change_by','penultimate_change_by'),)}),
    ]
    list_display = ('student', 'course', 'date_started')
    list_filter = ('course', 'date_started')
    readonly_fields = ('last_change_by','penultimate_change_by')
    
    def save_model(self, request, obj, form, change): 
        try:
            obj.last_change_by
        except:
            pass
        else:
            obj.penultimate_change_by = obj.last_change_by 
        obj.last_change_by = request.user 
        obj.save()

class GradeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('',{'fields':['student','subject','date_started','results',]}),
        ('Admin (non editable)', {'fields':(('last_change_by','penultimate_change_by'),)}),
    ]
    list_display = ('student','subject','date_started','results')
    list_filter = ('subject','date_started','results')
    readonly_fields = ('last_change_by','penultimate_change_by')
     
    def save_model(self, request, obj, form, change): 
        try:
            obj.last_change_by
        except:
            pass
        else:
            obj.penultimate_change_by = obj.last_change_by 
        obj.last_change_by = request.user 
        obj.save()
    
class ResultAdmin(admin.ModelAdmin):
    model = Result

    def save_model(self, request, obj, form, change): 
        try:
            obj.last_change_by
        except:
            pass
        else:
            obj.penultimate_change_by = obj.last_change_by 
        obj.last_change_by = request.user 
        obj.save()
    
class SessionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Subject and time', { 'fields': (('subject','date','session_number',),'timetable',)}),
    )
    list_display = ('subject', 'day_of_week','date','timetable','get_session_number_display')
    list_filter = ('date','session_number','students')
    inlines = [
        StaffAttendanceInline,
        StudentAttendanceInline,
    ]
    model = Session
    
    def save_formset(self, request, form, formset, change): 
        if formset.model == StudentAttendance:
            instances = formset.save(commit=False)
            for instance in instances:
                try:
                    instance.last_change_by
                except:
                    pass
                else:   
                    instance.penultimate_change_by = instance.last_change_by
                instance.last_change_by = request.user
                instance.save()
        else:
            formset.save()

class StaffAdminForm(ModelForm):
    class Meta:
        model = Staff
        widgets = {
            'dob': SelectDateWidget(years=BIRTH_YEARS),
            'gender': RadioSelect(),
        }            

class StaffAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Bio', { 'fields':(('first_name','surname'),('dob','gender'), ('island',))}),
        ('Contact Information', { 'fields':(('phone','email'),)}),
        ('Other Information', { 'fields':(('disability','disability_description'),('classification'))}),
        ('ISLPR', { 'fields':(('islpr_reading', 'islpr_writing', 'islpr_speaking', 'islpr_listening', 'islpr_overall'),)}),
        ('Admin (non editable)', {'fields':(('added', 'updated','last_change_by','penultimate_change_by'),)}),
    )
    form = StaffAdminForm
    list_display = ('__unicode__', 'gender', 'disability')
    list_filter = ('gender', 'disability')
    readonly_fields = ('added', 'updated','last_change_by','penultimate_change_by')
    inlines = (CredentialInline,
              )
    
    def save_model(self, request, obj, form, change): 
        try:
            obj.last_change_by
        except:
            pass
        else:
            obj.penultimate_change_by = obj.last_change_by 
        obj.last_change_by = request.user 
        obj.save()

    def save_formset(self, request, form, formset, change): 
        if formset.model == Credential:
            instances = formset.save(commit=False)
            for instance in instances:
                try:
                    instance.last_change_by
                except:
                    pass
                else:   
                    instance.penultimate_change_by = instance.last_change_by
                instance.last_change_by = request.user
                instance.save()
        else:
            formset.save()

class StudentAdminForm(ModelForm):
    class Meta:
        model = Student
        widgets = {
            'dob': SelectDateWidget(years=BIRTH_YEARS),
            'gender': RadioSelect(),
        }            

class StudentAdmin(admin.ModelAdmin):
    inlines = (EnrolmentInline,
               GradeInline,
               StudentAttendanceInline,
              )
    fieldsets = (
        ('Bio', { 'fields':(('first_name','surname'),('dob','gender'), ('island', 'slug'))}),
        ('Contact Information', { 'fields':(('phone','email'),)}),
        ('Other Information', { 'fields':(('disability','disability_description'), 'education_level', 'application_details')}),
        ('Admin (non editable)', {'fields':(('added', 'updated','last_change_by','penultimate_change_by'),)}),
    )
    form = StudentAdminForm
    list_display = ('__unicode__', 'slug', 'gender', 'disability')
    list_filter = ('gender', 'disability')
    ordering = ('-slug',) 
    readonly_fields = ('slug','added', 'updated','last_change_by','penultimate_change_by',)
    
    def save_model(self, request, obj, form, change): 
        try:
            obj.last_change_by
        except:
            pass
        else:
            obj.penultimate_change_by = obj.last_change_by 
        obj.last_change_by = request.user 
        obj.save()

    def save_formset(self, request, form, formset, change): 
        '''note that the following if isn't needed since all inlines use this, but is left as a bookmark'''
        if formset.model == Grade or formset.model == Enrolment or formset.model == StudentAttendance:
            instances = formset.save(commit=False)
            for instance in instances:
                try:
                    instance.last_change_by
                except:
                    pass
                else:   
                    instance.penultimate_change_by = instance.last_change_by
                instance.last_change_by = request.user
                instance.save()
        else:
            formset.save()

class SubjectAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', { 'fields': (('name','slug'),('year','semester'), 'staff_member')}),
    )

    list_display = ('name','year','semester')
    list_filter = ('year', 'semester', 'name')
    model = Subject
    prepopulated_fields = {'slug': ('name','year')}
    inlines = [ AssessmentInline, SessionInline, GradeInline,]
    
    def save_formset(self, request, form, formset, change): 
        if formset.model == Grade:
            instances = formset.save(commit=False)
            for instance in instances:
                try:
                    instance.last_change_by
                except:
                    pass
                else:   
                    instance.penultimate_change_by = instance.last_change_by
                instance.last_change_by = request.user
                instance.save()
        else:
            formset.save()

class TimetableAdmin(admin.ModelAdmin):
    model = Timetable
    prepopulated_fields = {'slug': ('year','term')}

admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Credential, CredentialAdmin)
admin.site.register(Enrolment, EnrolmentAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(StaffAttendance)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentAttendance, StudentAttendanceAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Timetable, TimetableAdmin)
