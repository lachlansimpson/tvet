from django.db import models
from django.template.defaultfilters import slugify
import datetime
import calendar

today = datetime.date.today() # used by the Attendance record

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
    (u'0',u'Present'),
    (u'1',u'Absent'),
    (u'2',u'Late'),
    (u'3',u'Withdrawn'),
)

ABSENCE_CHOICES = (
    (u'0',u'Sick'),
    (u'1',u'Medical Certificate'),
    (u'2',u'KIT Official'),
    (u'3',u'Compassionate'),
    (u'4',u'Unexplained'),
)

SUBJECT_RESULTS = (
    (u'P',u'Pass'),
    (u'F',u'Fail'),
)

COURSE_RESULTS = (
    (u'P',u'Pass'),
    (u'F',u'Fail'),
)

class Timetable(models.Model):
    class Meta:
        unique_together = ('year','term')

    year = models.IntegerField()
    term = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    slug = models.SlugField(max_length=12)
    
    def __unicode__(self):
        '''Timetable reference: year and term number'''
        return str(self.year) + ', Term ' + str(self.term)
    
    @models.permalink	
    def get_absolute_url(self):
        return ('timetable_view', [str(self.slug)])

class Session(models.Model):
    session_number = models.CharField(max_length=1,choices=SESSION_CHOICES)
    subject = models.ForeignKey('Subject')
    timetable = models.ForeignKey(Timetable, related_name='sessions')
    date = models.DateField()

    def __unicode__(self):
        '''Session Reference: day of week, date, term/year (Timetable)'''
        date_readable = self.day_of_week() + ', ' + str(self.date.day) + ' ' + calendar.month_name[self.date.month]
        return str(self.timetable) + ', ' + date_readable + ', '+ str(self.subject.name)

    def timetable_listing(self):
        ''' returns date-free name for session to be put into timetable '''
        return str(self.subject.name)

    def day_of_week(self):
        day_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        return day_names[self.date.weekday()] 

class Person(models.Model):
    '''Abstract Class under Student and Staff'''
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40, editable=False, blank=True)
    dob = models.DateField('Date of Birth')  
    gender = models.CharField(max_length='1', choices=GENDER_CHOICES,
                              default='F')
    phone = models.CharField(max_length=12, blank=True)
    email = models.EmailField(blank=True)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        """Person reference: full name """
        return self.first_name + ' ' + self.surname

    def first_letter(self):
        return self.surname and self.surname[0] or ''

class Student(Person):
    '''Represents each student '''
    def get_id(self):
        ''' 
        This returns the student's DB reference number, or "student number"
        Not kept in the database as it would be extraneous
        The 100000 is added for aesthetic reasons only
        '''
        return self.pk + 100000

    def save(self):
        '''Can't use prepopulated_fields due to function's restrictions
        Set the Slug to student ID number''' 
        if not self.pk:
            super(Student, self).save() # Call the first save() method to get pk
            self.slug = slugify(self.get_id())
        super(Student, self).save() # Call the "real" save() method.

    @models.permalink	
    def get_absolute_url(self):
        return ('student_view', [str(self.slug)])

class Staff(Person):
    '''Respresents each Staff member'''
    def get_id(self):
        return self

    def save(self):
        self.slug = slugify(self) #slugify staff members name
        super(Staff, self).save() 

    @models.permalink	
    def get_absolute_url(self):
        return ('staff_view', [str(self.slug)])

class Subject(models.Model):
    '''Represents individual subjects, classes, cohorts'''
    ''' TODO: name it UNIT OF COMPETENCE '''
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)
    semester = models.CharField(max_length=1, blank=True, choices=SEMESTER_CHOICES)
    year = models.IntegerField()
    members = models.ManyToManyField(Student, through='Grade', blank=True, null=True)

    def __unicode__(self):
        '''Subject reference: subject name and the year given'''
        return self.name + ', ' + str(self.year) 

    @models.permalink	
    def get_absolute_url(self):
        return ('subject_view', [str(self.slug)])

class Course(models.Model):
    '''Represents Courses - a collection of subjects leading to a degree'''
    ''' TODO: aka Qualifications'''
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)
    students = models.ManyToManyField(Student, through='Enrolment', blank=True, null=True)
    subjects = models.ManyToManyField(Subject, blank=True, null=True)

    def __unicode__(self):
        '''Course Reference: name of the course'''
        return self.name

    @models.permalink	
    def get_absolute_url(self):
        return ('course_view', [str(self.slug)])

class SubjectResults(models.Model):
    '''Represents an Assignment and it's results'''
    name = models.CharField(max_length=30)
    date = models.DateField()
    mark = models.CharField(max_length=2, choices=SUBJECT_RESULTS)    

    class Meta:
        verbose_name = 'Subject Results'
        verbose_name_plural = 'Subject Results'

    def __unicode__(self):
        '''SubjectResults reference: the assignment name, due date and grade given'''
        return self.name + ', ' + str(self.date) + ', ' + str(self.grade)

    @models.permalink	
    def get_absolute_url(self):
        return ('subjectresults_view', [str(self.slug)])

class Attendance(models.Model):
    '''Represents the "roll call" or attendance record'''
    session = models.ManyToManyField(Session)
    reason = models.CharField(max_length=1, choices=REASON_CHOICES, default='P')
    absent = models.CharField(max_length=1, choices=ABSENCE_CHOICES, blank=True)

    def __unicode__(self):
        '''Attendance reference: returns date, session and reason'''
        return self.session + ', ' + self.get_reason_display()
        #return str(self.session) + ', ' + self.get_reason_display()

    @models.permalink	
    def get_absolute_url(self):
        return ('attendance_view', [str(self.slug)])

class Enrolment(models.Model):
    '''Represents a Student's enrolment in a Course'''
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    date_started = models.DateField()
    date_ended = models.DateField(blank=True, null=True)
    mark = models.CharField(max_length=1, choices=COURSE_RESULTS, blank=True)
    slug = models.SlugField(max_length=40, blank=True)

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

    def save(self):
        '''Can't use prepopulated_fields due to function's restrictions
        using the unique combination of student, course and year started
        '''
        year_started = self.date_started.year
        slug_str = str(self.student) + ' ' + str(self.course) + ' ' + str(year_started)
        self.slug = slugify(slug_str)
        super(Enrolment, self).save() 

class Grade(models.Model):
    '''Represents a Student's interactions with a Subject. ie, being in a class.'''
    student = models.ForeignKey(Student)
    subject = models.ForeignKey(Subject)
    date_started = models.DateField()
    results = models.ForeignKey(SubjectResults, blank=True, null=True)
    attendance = models.ManyToManyField(Attendance, blank=True, null=True) 
    slug = models.SlugField(max_length=60)

    def __unicode__(self):
        '''Grade reference: student's name and subject '''
        return str(self.student) + ', ' + str(self.subject)
    
    @models.permalink	
    def get_absolute_url(self):
        return ('grade_view', [str(self.slug)])

    def save(self):
        '''Can't use prepopulated_fields due to function's restrictions
        using the unique combination of student, subject and year they started
        the class'''
        year_started = self.date_started.year()
        slug_temp = self.student + self.subject + str(year_started)
        self.slug = slugify(slug_temp)
        super(Grade, self).save() 
