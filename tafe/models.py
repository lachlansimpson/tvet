from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime

today = datetime.date.today() # used by the Attendance record

ISLAND_CHOICES = (
    ('Tarawa',u'Tarawa'),
    ('Abaiang',u'Abaiang'),
    ('Kiritimati',u'Kiritimati'),
    ('Makin',u'Makin'),
    ('Butaritari',u'Butaritari'),
    ('Marakei',u'Marakei'),
    ('Maiana',u'Maiana'),
    ('Kuria',u'Kuria'),
    ('Aranuka',u'Aranuka'),
    ('Abemana',u'Abemana'),
    ('Nonouti',u'Nonouti'),
    ('Tabiteua',u'Tabiteua'),
    ('Onotoa',u'Onotoa'),
    ('Beru',u'Beru'),
    ('Nikunau',u'Nikunau'),
    ('Tamana',u'Tamana'),
    ('Arorae',u'Arorae'),
    ('Banaba',u'Banaba'),
    ('Teraina',u'Teraina'),
    ('Kanton',u'Kanton'),
    ('Tabuaeran',u'Tabuaeran'),
    ('Other',u'Other'),
    ('Internatio',u'International'),
)

GENDER_CHOICES = (
    (u'M',u'Male'),
    (u'F',u'Female'),
)

SEMESTER_CHOICES = (
    (u'1',u'First'),
    (u'2',u'Second'),
    (u'B',u'Both'),
)

SESSION_CHOICES = (
    (u'0',u'Morning 1'),
    (u'1',u'Morning 2'),
    (u'2',u'Afternoon 1'),
    (u'3',u'Afternoon 2'),
    (u'4',u'Evening'),
    (u'5',u'Weekend'),
)

REASON_CHOICES = (
    (u'P',u'Present'),
    (u'A',u'Absent'),
    (u'L',u'Late'),
    (u'W',u'Withdrawn'),
)

ABSENCE_CHOICES = (
    (u'S',u'Sick'),
    (u'M',u'Medical Certificate'),
    (u'K',u'KIT Official'),
    (u'C',u'Compassionate'),
    (u'U',u'Unexplained'),
)

SUBJECT_RESULTS = (
    (u'P',u'Pass'),
    (u'F',u'Fail'),
)

COURSE_RESULTS = (
    (u'P',u'Pass'),
    (u'F',u'Fail'),
    (u'W',u'Withdrawn'),
)

CLASSIFICATION_CHOICES = (
    ('T', 'Trainer'),
    ('M', 'Manager'),
)

AQF_LEVEL_CHOICES = (
    ('BHONS','Bachelor Honors'),
    ('GCERT','Graduate Certificate'),
    ('GDIP','Graduate Diploma'), 
    ('BACH','Bachelor'),
    ('ADIP','Advanced Diploma'),
    ('ADEG','Associate Degree'),
    ('DIP','Diploma'),
    ('CERT4','IV'),
    ('CERT3','III'),
    ('CERT2','II'),
    ('CERT1','I'),
    ('PHD','Doctoral'),
    ('MAST','Masters'),
    ('OTH','Other'),
)

CREDENTIAL_TYPE_CHOICES = (
    ('E','Education'),
    ('T','Training'),
    ('V','Vocational'),
    ('L','English'),
)

ISLPR_CHOICES = (
    ('0','0 Zero Proficiency'),
    ('0+','0+ Formulaic Proficiency'),
    ('1-','1- Minimum Proficiency'),
    ('1','1 Basic Proficiency'),
    ('1+','1+ Transactional Proficiency'),
    ('2','2 Basic Social Proficiency'),
    ('2+','2+ Social Proficiency'),
    ('3','3 Basic Vocational Proficiency'),
    ('3+','3+ Basic Vocational Proficiency Plus'),
    ('4', '4 Vocational Proficiency'),
    ('4+','4+ Advanced Vocational Proficiency'),
    ('5','5 Native Proficiency'),
)

EDUCATION_LEVEL_CHOICES = (
    ('0','PSSC - Post Secondary School Certificate'),
    ('1','KNC - Kiribati National certificate'),
    ('2','USP - University of South Pacific - Extension; Degree; Post Graduate'),
    ('3','JSSC - Junior School Certificate - Form 3'), 
    ('4','Form 4'),
    ('5','Form 5'),
    ('6','Form 6'),
    ('7','Form 7'),
    ('8','SPFSC - Fiji School Certificate'),
    ('9','Form 3 or below'),
)

ROOM_CHOICES = (
    ('Room 1', 'Room 1'),
    ('Room 2', 'Room 2'),
    ('Room 3', 'Room 3'),
    ('Room 4', 'Room 4'),
    ('Room 5', 'Room 5'),
    ('Room 6', 'Room 6'),
)

class AttendanceBeforeTodayManager(models.Manager):
    def get_query_set(self):
        attendance_list = super(AttendanceBeforeTodayManager, self).get_query_set().filter(session_date__gte=today)
        return attendance_list

class Attendance(models.Model):
    '''Represents the "roll call" or attendance record'''
    reason = models.CharField(max_length=1, choices=REASON_CHOICES, blank=True)
    absent = models.CharField(max_length=1, choices=ABSENCE_CHOICES, blank=True)
    slug = models.SlugField(blank=True)
    session = models.ForeignKey('Session', related_name='%(class)s_attendance_records')

    last_change_by = models.ForeignKey(User, related_name='%(class)s_last_change_by', editable=False)
    penultimate_change_by = models.ForeignKey(User, related_name='%(class)s_penultimate_change_by', blank=True, null=True,editable=False)
    objects = models.Manager()
    attendance_before_today = AttendanceBeforeTodayManager()

    class Meta:
        abstract = True

    @models.permalink	
    def get_absolute_url(self):
        return ('attendance_view', (), {
            'year': self.date.year,
            'month': self.date.month,
            'day': self.date.day,
            'session': self.session.slug, 
            'slug': self.slug})
        
class StudentAttendance(Attendance):
    student = models.ForeignKey('Student', related_name='attendance_records')

    class Meta:
        verbose_name='Student Attendence Record'
        verbose_name_plural='Student Attendence Records'
    
    def __unicode__(self):
        '''Attendance reference: returns date, session and reason'''
        return str(self.session) + ', ' + self.get_reason_display()

    def save(self, *args, **kwargs):
        slug_temp = self.session.slug + ' ' + self.student.slug
        self.slug = slugify(slug_temp)
        super(StudentAttendance, self).save(*args, **kwargs)
    
class StaffAttendance(Attendance):
    staff_member = models.ForeignKey('Staff', related_name='attendance_records')
    
    class Meta:
        verbose_name='Staff Attendence Record'
        verbose_name_plural='Staff Attendence Records'
    
    def __unicode__(self):
        '''Attendance reference: returns date, session and reason'''
        return self.staff + ' ' + self.session + ' ' + self.get_reason_display()

    def save(self, *args, **kwargs):
        slug_temp = self.session.slug + ' ' + self.staff_member.slug
        self.slug = slugify(slug_temp)
        super(StaffAttendance, self).save(*args, **kwargs)
    
class FemaleManager(models.Manager):
    def get_query_set(self):
        return super(FemaleManager, self).get_query_set().filter(gender='F')

class MaleManager(models.Manager):
    def get_query_set(self):
        return super(MaleManager, self).get_query_set().filter(gender='M')

class ISLPR_record(models.Model):
    islpr_reading = models.CharField('Reading Level', max_length=2, choices=ISLPR_CHOICES)
    islpr_writing = models.CharField('Writing Level', max_length=2, choices=ISLPR_CHOICES)
    islpr_speaking = models.CharField('Speaking Level', max_length=2, choices=ISLPR_CHOICES)
    islpr_listening = models.CharField('Listening Level', max_length=2, choices=ISLPR_CHOICES)
    islpr_overall = models.CharField('Overall', max_length=2, choices=ISLPR_CHOICES)
    date_tested = models.DateField()
    
    class Meta:
        abstract = True
        '''TODO: HOWTO make ISLPR all caps'''
        verbose_name = 'ISLPR record'
        verbose_name_plural = 'ISLPR records'

class StudentISLPR(ISLPR_record):
    student = models.ForeignKey('Student', related_name='islpr_record')

class StaffISLPR(ISLPR_record):
    staff_member = models.ForeignKey('Staff', related_name='islpr_record')

class Person(models.Model):
    '''Abstract Class under Applicant, Student and Staff'''
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    slug = models.SlugField('ID number', max_length=40, editable=False, blank=True)
    dob = models.DateField('Date of Birth')  
    gender = models.CharField(max_length='1', choices=GENDER_CHOICES, default='F')
    island = models.CharField(max_length='10', choices=ISLAND_CHOICES, default='Tarawa', blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True)
    phone2 = models.CharField(max_length=12, blank=True)
    email = models.EmailField(blank=True)
    
    disability = models.NullBooleanField()
    disability_description = models.CharField('Description', max_length=50, blank=True)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_change_by = models.ForeignKey(User, related_name='%(class)s_last_change_by', editable=False, blank=True,  null=True)
    penultimate_change_by = models.ForeignKey(User, related_name='%(class)s_penultimate_change_by', blank=True, null=True, editable=False)

    people = models.Manager()
    men = MaleManager()
    women = FemaleManager()
    
    class Meta:
        abstract = True

    def __unicode__(self):
        """Person reference: full name """
        return self.first_name + ' ' + self.surname

    def age_today(self):
        return today.year - self.dob.year

    def first_letter(self):
        return self.first_name and self.first_name[0] or ''

class CurrentApplicantManager(models.Manager):
    def get_query_set(self):
        return super(CurrentApplicantManager, self).get_query_set().exclude(successful='1').exclude(successful='0').order_by('first_name')


class Applicant(Person):
    applied_for = models.ForeignKey('Course', related_name='applicants')
    education_level = models.CharField(max_length=2, blank=True, choices=EDUCATION_LEVEL_CHOICES)
    successful = models.NullBooleanField()
    short_listed = models.NullBooleanField()
    test_ap = models.IntegerField('Application test result', blank=True, null=True)
    test_ma = models.IntegerField('Maths test result', blank=True, null=True)
    test_eng = models.IntegerField('English test result', blank=True, null=True)
    other_courses = models.TextField('Other Courses', blank=True)
    experience = models.TextField('Previous experience', blank=True)
    ranking = models.IntegerField(blank=True, null=True)
    eligibility = models.NullBooleanField()
    date_of_application = models.DateField(blank=True, null=True)
    date_offer_sent = models.DateField(blank=True, null=True)
    date_offer_accepted = models.DateField(blank=True, null=True)

    objects = models.Manager()
    current = CurrentApplicantManager()

    @models.permalink
    def get_absolute_url(self):
        return ('applicant_view', [str(self.slug)])
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super(Applicant, self).save(*args, **kwargs) # Call the first save() method to get pk
            self.slug = slugify(str(self))
        super(Applicant, self).save(*args, **kwargs) # Call the "real" save() method.

    def age_group(self):
        if self.age_today < 25:
            return '16-24'
        elif self.age_today < 36:
            return '25-35'
        return '35+'
    
    def convert_to_student(self):
        '''Turn an applicant into a student, create all required associated objects'''
        if self.successful:
            '''already converted'''
            pass 
        else:
            '''not converted, let's go!'''
            '''create the Student object, transfer all data'''
            new_student = Student()
            new_student.first_name = self.first_name
            new_student.surname = self.surname
            new_student.dob = self.dob
            new_student.gender = self.gender
            new_student.island = self.island
            new_student.phone = self.phone
            new_student.email = self.email
            new_student.disability = self.disability
            new_student.disability_description = self.disability_description

            new_student.education_level = self.education_level            
            new_student.application_details_id = self.pk
            new_student.save()

            '''Create the Enrolment record for the Student and the Course they applied for'''
            new_enrolment = Enrolment()
            new_enrolment.student = new_student
            new_enrolment.course = self.applied_for
            new_enrolment.save()
            
            '''At the moment all units/subjects in a course are compulsory - 
            this method will need to change for greater flexibility in the future'''
            ''' Create the Grade object for each unit in the course, related to the 
            student object'''
            for unit in self.applied_for.subjects.all():
                new_grade = Grade()
                new_grade.student = new_student
                new_grade.subject = unit
                new_grade.date_started = today
                new_grade.save()
                
            '''Converted successfully, move along'''
            self.successful= 1 
            self.save()

class Assessment(models.Model):
    name = models.CharField(max_length=50)
    date_given = models.DateField()
    date_due = models.DateField()
    subject = models.ForeignKey('Subject', related_name="assessments")
    slug = models.CharField(max_length=50)

    def __unicode__(self):
        return self.subject.name + ', ' + self.name + ', ' + str(self.date_due)

    def get_absolute_url(self):
        return self.subject.get_absolute_url() + "assessment/" + self.slug

    def get_year(self):
        return self.date_due.year

class Subject(models.Model):
    '''Represents individual subjects, classes, cohorts'''
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)
    semester = models.CharField(max_length=1, blank=True, choices=SEMESTER_CHOICES)
    year = models.IntegerField()
    staff_member = models.ForeignKey('Staff', blank=True, null=True)
    students = models.ManyToManyField('Student', through='Grade', blank=True, null=True)

    class Meta:
        verbose_name='Unit of Competence'
        verbose_name_plural='Units of Competence'
    
    def __unicode__(self):
        '''Subject reference: subject name and the year given'''
        return self.name + ', ' + str(self.year) 

    @models.permalink	
    def get_absolute_url(self):
        return ('unit_view', [str(self.slug)])

    def first_letter(self):
        return self.name and self.name[0] or ''

    def this_weeks_sessions(self):
        '''These are used to return this week's sessions'''
        last_monday = today - datetime.timedelta(days=today.weekday())
        this_friday = today + datetime.timedelta( (4-today.weekday()) % 7 )
        this_weeks_sessions = []
        for session in self.sessions.all(): 
            if session.date > last_monday and session.date < this_friday:
                this_weeks_sessions.append(session)
        return this_weeks_sessions

class Course(models.Model):
    '''Represents Courses - a collection of subjects leading to a degree'''
    name = models.CharField(max_length=30)
    year = models.CharField(max_length=4)
    slug = models.SlugField(max_length=40)
    students = models.ManyToManyField('Student', through='Enrolment', blank=True, null=True)
    subjects = models.ManyToManyField('Subject', related_name='courses', blank=True, null=True, verbose_name=Subject._meta.verbose_name_plural)

    class Meta:
        verbose_name='Qualification'
        verbose_name_plural='Qualifications'

    def __unicode__(self):
        '''Course Reference: name of the course'''
        return str(self.name)

    @models.permalink	
    def get_absolute_url(self):
        return ('course_view', [str(self.slug)])

    def count_students(self):
        return self.students.count()

    def count_males(self):
        return self.students.filter(gender='M').count()

    def count_females(self):
        return self.students.filter(gender='F').count()

    def subjects_available(self):
        list = ''
        for subject in self.subjects.all():
            if list == '':
                list = subject.name
            else:
                list += ', ' + subject.name
        return list 

class Credential(models.Model):
    ''' This is the class of objects to represent what qualifications the staff have'''
    name = models.CharField(max_length=50)
    aqf_level = models.CharField('AQF Level', max_length=5, choices=AQF_LEVEL_CHOICES)
    institution = models.CharField(max_length=40)
    year = models.CharField(max_length=4)
    type = models.CharField(max_length=1, choices=CREDENTIAL_TYPE_CHOICES)

    last_change_by = models.ForeignKey(User, related_name='%(class)s_last_change_by', editable=False)
    penultimate_change_by = models.ForeignKey(User, related_name='%(class)s_penultimate_change_by', blank=True, null=True, editable=False)

    class Meta:
        verbose_name_plural='Credentials'
    
    def __unicode__(self):
        return str(self.get_aqf_level_display()) +', '+self.name+', '+self.institution

class Enrolment(models.Model):
    '''Represents a Student's enrolment in a Course'''
    student = models.ForeignKey('Student', related_name='enrolments')
    course = models.ForeignKey(Course, related_name='enrolments')
    date_started = models.DateField(default=today)
    date_ended = models.DateField(blank=True, null=True)
    mark = models.CharField(max_length=1, choices=COURSE_RESULTS, blank=True)
    withdrawn_reason = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=40, blank=True)

    last_change_by = models.ForeignKey(User, related_name='%(class)s_last_change_by', editable=False, blank=True, null=True)
    penultimate_change_by = models.ForeignKey(User, related_name='%(class)s_penultimate_change_by', blank=True, null=True, editable=False)
    
    def __unicode__(self):
        '''
        Enrolment reference: return the student's name, the course name, the date started
            if the Enrolment has a end date, add it to the end
            if the Enrolment has a mark/grade, add it to the end
        '''
        enrol = str(self.student) +', ' + str(self.course) + ', ' + str(self.date_started) 
        if self.date_ended:
            enrol + ', ' + self.date_ended
        if self.mark:
            enrol + ', ' + self.get_course_results_display()
        return enrol

    @models.permalink	
    def get_absolute_url(self):
        return ('enrolment_view', [str(self.slug)])

    def save(self, *args, **kwargs):
        '''SLUG:Can't use prepopulated_fields due to function's restrictions
        using the unique combination of student, course and year started
        '''
        year_started = self.date_started.year
        slug_str = str(self.student) + ' ' + str(self.course) + ' ' + str(year_started)
        self.slug = slugify(slug_str)
        super(Enrolment, self).save(*args, **kwargs) 
#        if self.mark == 'W':
#            pass
    
#    def is_valid(self):
#        if self.mark == 'W':
#
#        super(Enrolment, self)

class Grade(models.Model):
    '''Represents a Student's interactions with a Subject. ie, being in a class.'''
    student = models.ForeignKey('Student', related_name='grades')
    subject = models.ForeignKey('Subject', related_name='grades')
    date_started = models.DateField()
    results = models.ForeignKey('Result', related_name='grades', blank=True, null=True)
    slug = models.SlugField(max_length=60)

    last_change_by = models.ForeignKey(User, related_name='%(class)s_last_change_by', editable=False)
    penultimate_change_by = models.ForeignKey(User, related_name='%(class)s_penultimate_change_by', blank=True, null=True, editable=False)
    
    def __unicode__(self):
        '''Grade reference: student's name and subject '''
        return str(self.student) + ', ' + str(self.subject)
    
    @models.permalink	
    def get_absolute_url(self):
        return ('grade_view', [str(self.slug)])

    def save(self, *args, **kwargs):
        '''Can't use prepopulated_fields due to function's restrictions
        using the unique combination of student, subject and year they started
        the class'''
        slug_temp = str(self.student) + ' ' +str(self.subject)
        self.slug = slugify(slug_temp)
        super(Grade, self).save(*args, **kwargs) 

class Result(models.Model):
    '''Represents an Assignment and it's results'''
    assessment = models.ForeignKey('Assessment')
    date_submitted = models.DateField()
    mark = models.CharField(max_length=2, choices=SUBJECT_RESULTS)    
    
    last_change_by = models.ForeignKey(User, related_name='%(class)s_last_change_by', editable=False)
    penultimate_change_by = models.ForeignKey(User, related_name='%(class)s_penultimate_change_by', blank=True, null=True,editable=False)
    
    class Meta:
        verbose_name='Result'
        verbose_name_plural='Results'
    
    def __unicode__(self):
        '''Result reference: the assignment name, due date and grade given'''
        return self.assessment.name + ', ' + str(self.date_submitted)

    @models.permalink	
    def get_absolute_url(self):
        return ('result_view', [str(self.slug)])

class Session(models.Model):
    session_number = models.CharField(max_length=1,choices=SESSION_CHOICES)
    subject = models.ForeignKey('Subject', related_name='sessions')
    timetable = models.ForeignKey('Timetable', related_name='sessions')
    date = models.DateField()
    slug = models.SlugField(max_length=50, blank=True)
    students = models.ManyToManyField('Student', through='StudentAttendance', blank=True, null=True)
    room_number = models.CharField(max_length=7, choices=ROOM_CHOICES, blank=True)

    def __unicode__(self):
        '''Session Reference: day of week, date, term/year (Timetable)'''
        return str(self.subject.name) + ', ' + self.day_of_week() + ', ' + self.get_session_number_display() + ', '+ ' ' + str(self.date)

    def timetable_listing(self):
        ''' returns date-free name for session to be put into timetable '''
        return str(self.subject.name)

    def day_of_week(self):
        day_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        return day_names[self.date.weekday()] 

    @models.permalink
    def get_absolute_url(self):
        return ('session_view', (), {
            'year': self.date.year,
            'month': self.date.month,
            'day': self.date.day,
            'slug': self.slug})
    
    def save(self, *args, **kwargs):
        slug_temp = str(self.subject.name) + " " + self.get_session_number_display()
        self.slug = slugify(slug_temp)
        super(Session, self).save(*args, **kwargs) 

class Staff(Person):
    '''Respresents each Staff member'''
    classification = models.CharField(max_length=2, choices=CLASSIFICATION_CHOICES)
    credential = models.ManyToManyField('Credential', blank=True, null=True, related_name='credentials')

    class Meta:
        verbose_name='Staff'
        verbose_name_plural='Staff'

    def __unicode__(self):
        return self.first_name +' ' + self.surname
    
    def get_id(self):
        return self

    def save(self, *args, **kwargs):
        self.slug = slugify(self) #slugify staff members name
        super(Staff, self).save(*args, **kwargs) 

    @models.permalink	
    def get_absolute_url(self):
        return ('staff_view', [str(self.slug)])

class NewStudentManager(models.Manager):
    def get_query_set(self):
        return super(NewStudentManager, self).get_query_set().filter(enrolment__student__isnull=True)

class Student(Person):
    '''Represents each student '''
    education_level = models.CharField(max_length=2, blank=True, choices=EDUCATION_LEVEL_CHOICES)
    application_details = models.ForeignKey('Applicant')
    
    objects = models.Manager()
    new_students = NewStudentManager()

    def get_id(self):
        ''' 
        This returns the student's DB reference number, or "student number"
        Not kept in the database as it would be extraneous
        The 100000 is added for aesthetic reasons only
        '''
        return self.pk + 100000

    def save(self, *args, **kwargs):
        '''Can't use prepopulated_fields due to function's restrictions
        Set the Slug to student ID number''' 
        if not self.pk:
            super(Student, self).save(*args, **kwargs) # Call the first save() method to get pk
            self.slug = slugify(self.get_id())
        super(Student, self).save(*args, **kwargs) # Call the "real" save() method.

    @models.permalink	
    def get_absolute_url(self):
        return ('student_view', [str(self.slug)])

    def attendance_before_today(self):
        l = self.attendance_records.exclude(session__date__gte =today).order_by('-session__date')
        return l

class Timetable(models.Model):
    year = models.IntegerField()
    term = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    slug = models.SlugField(max_length=12)
    
    class Meta:
        unique_together = ('year','term')

    def __unicode__(self):
        '''Timetable reference: year and term number'''
        return str(self.year) + ', Term ' + str(self.term)
    
    @models.permalink	
    def get_absolute_url(self):
        return ('timetable_view', [str(self.slug)])
