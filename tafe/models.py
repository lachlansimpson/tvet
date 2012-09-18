from django.db import models
from django.template.defaultfilters import slugify
import datetime

today = datetime.date.today() # used by the Attendance record

ISLAND_CHOICES = (
    ('01',u'Tarawa'),
    ('02',u'Abaiang'),
    ('03',u'Kiritimati'),
    ('04',u'Makin'),
    ('05',u'Butaritari'),
    ('06',u'Marakei'),
    ('07',u'Maiana'),
    ('08',u'Kuria'),
    ('09',u'Aranuka'),
    ('10',u'Abemana'),
    ('11',u'Nonouti'),
    ('12',u'Tabiteua'),
    ('13',u'Onotoa'),
    ('14',u'Beru'),
    ('15',u'Nikunau'),
    ('16',u'Tamana'),
    ('17',u'Arorae'),
    ('18',u'Banaba'),
    ('19',u'Teraina'),
    ('20',u'Kanton'),
    ('21',u'Tabuaeran'),
    ('22',u'Other'),
    ('23',u'International'),
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
    subject = models.ForeignKey('Subject', related_name='sessions')
    timetable = models.ForeignKey(Timetable, related_name='sessions')
    date = models.DateField()
    slug = models.SlugField(max_length=50,blank=True)
    students = models.ManyToManyField('Student', through='Attendance', blank=True, null=True)

    def __unicode__(self):
        '''Session Reference: day of week, date, term/year (Timetable)'''
        return self.day_of_week() + ', ' + self.get_session_number_display() + ', '+ str(self.subject.name) + ' ' + str(self.date)

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
    
    def save(self):
        slug_temp = str(self.subject.name) + " " + self.get_session_number_display()
        self.slug = slugify(slug_temp)
        super(Session, self).save() 

class FemaleManager(models.Manager):
    def get_query_set(self):
        return super(FemaleManager, self).get_query_set().filter(gender='F')

class MaleManager(models.Manager):
    def get_query_set(self):
        return super(MaleManager, self).get_query_set().filter(gender='M')

class Person(models.Model):
    '''Abstract Class under Student and Staff'''
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    slug = models.SlugField('ID number', max_length=40, editable=False, blank=True)
    dob = models.DateField('Date of Birth')  
    gender = models.CharField(max_length='1', choices=GENDER_CHOICES, default='F')
    island = models.CharField(max_length='2', choices=ISLAND_CHOICES, default='01', blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True)
    email = models.EmailField(blank=True)
    
    disability = models.BooleanField()
    disability_description = models.CharField('Description', max_length=50, blank=True)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    people = models.Manager()
    men = MaleManager()
    women = FemaleManager()
    
    class Meta:
        abstract = True

    def __unicode__(self):
        """Person reference: full name """
        return self.first_name + ' ' + self.surname

    def first_letter(self):
        return self.surname and self.surname[0] or ''

    def age_today(self):
        return today.year() - self.dob.year()

#TODO Check how to filter by reverse FK
class NewStudentManager(models.Manager):
    def get_query_set(self):
        return super(NewStudentManager, self).get_query_set().filter(enrolment__student__isnull=True)

class Student(Person):
    '''Represents each student '''
    education_level = models.CharField(max_length=50, blank=True)
    
    objects = models.Manager()
    new_students = NewStudentManager()

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

class Applicant(Person):
    applied_for = models.ForeignKey('Course', related_name='applicants')
    education_level = models.CharField(max_length=50, blank=True)
    successful = models.BooleanField()
    short_listed = models.BooleanField()
    test_ap = models.IntegerField('AP test result', blank=True, null=True)
    test_ma = models.IntegerField('MA test result', blank=True, null=True)
    test_eng = models.IntegerField('English test result', blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)
    eligibility = models.BooleanField()
    date_offer_sent = models.DateField(blank=True, null=True)
    date_offer_accepted = models.DateField(blank=True, null=True)
    objects = models.Manager()

    @models.permalink
    def get_absolute_url(self):
        return ('applicant_view', [str(self.slug)])
    
    def save(self):
        if not self.pk:
            super(Applicant, self).save() # Call the first save() method to get pk
            self.slug = slugify(str(self))
        super(Applicant, self).save() # Call the "real" save() method.

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
            new_student.education_level = self.education_level
            new_student.save()

            '''Create the Enrolment record for the Student and the Course they applied for'''
            new_enrolment = Enrolment()
            new_enrolment.student = self
            new_enrolment.course = self.applied_for
            new_enrolment.save()
            
            '''At the moment all units/subjects in a course are compulsory - 
            this method will need to change for greater flexibility in the future'''
            ''' Create the Grade object for each unit in the course, related to the 
            student object'''
            for unit in self.applied_for.subjects:
                new_grade = Grade()
                new_grade.student = self
                new_grade.subject = unit
                new_grade.date_started = today
                new_grade.save()

                ''' For each grade, there is a session object per date
                To which is attached an attendance record per student
                Create all attendance records in advance'''
                for session in unit.sessions:
                    new_attendance_record = Attendance()
                    new_attendance_record.student = self
                    new_attendance_record.subject = unit
                    new_attendance_record.save()

            '''Converted successfully, move along'''
            self.successful='True'

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
    class Meta:
        verbose_name='Unit of Competence'
        verbose_name_plural='Units of Competence'
    
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

    def first_letter(self):
        return self.name and self.name[0] or ''

class Course(models.Model):
    '''Represents Courses - a collection of subjects leading to a degree'''
    class Meta:
        verbose_name='Qualification'
        verbose_name_plural='Qualifications'

    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)
    students = models.ManyToManyField(Student, through='Enrolment', blank=True, null=True)
    subjects = models.ManyToManyField(Subject, related_name='courses', blank=True, null=True)

    def __unicode__(self):
        '''Course Reference: name of the course'''
        return self.name

    @models.permalink	
    def get_absolute_url(self):
        return ('course_view', [str(self.slug)])

    def count_students(self):
        return self.students.count()

    def count_males(self):
        return self.students.men().count()

    def count_females(self):
        return self.students.women().count()

    def subjects_available(self):
        list = ''
        for subject in self.subjects.all():
            if list == '':
                list = subject.name
            else:
                list += ', ' + subject.name
        return list 

class SubjectResults(models.Model):
    '''Represents an Assignment and it's results'''
    class Meta:
        verbose_name='Result'
        verbose_name_plural='Results'
    
    name = models.CharField(max_length=30)
    date = models.DateField()
    mark = models.CharField(max_length=2, choices=SUBJECT_RESULTS)    

    def __unicode__(self):
        '''SubjectResults reference: the assignment name, due date and grade given'''
        return self.name + ', ' + str(self.date) + ', ' + str(self.grade)

    @models.permalink	
    def get_absolute_url(self):
        return ('subjectresults_view', [str(self.slug)])

class Attendance(models.Model):
    '''Represents the "roll call" or attendance record'''
    class Meta:
        verbose_name='Attendence Record'
        verbose_name_plural='Attendence Records'
    
    session = models.ForeignKey(Session, related_name='attendance_records')
    student = models.ForeignKey(Student, related_name='attendance_records')
    reason = models.CharField(max_length=1, choices=REASON_CHOICES, default='P')
    absent = models.CharField(max_length=1, choices=ABSENCE_CHOICES, blank=True)
    slug = models.SlugField(blank=True)

    def __unicode__(self):
        '''Attendance reference: returns date, session and reason'''
        return str(self.session) + ', ' + self.get_reason_display()

    def save(self):
        slug_temp = self.session.slug + ' ' + self.student.slug
        self.slug = slugify(slug_temp)
        super(Attendance, self).save()
    
    @models.permalink	
    def get_absolute_url(self):
        return ('attendance_view', [str(self.slug)])

class Enrolment(models.Model):
    '''Represents a Student's enrolment in a Course'''
    student = models.ForeignKey(Student, related_name='enrolments')
    course = models.ForeignKey(Course, related_name='enrolments')
    date_started = models.DateField(default=today)
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
    student = models.ForeignKey(Student, related_name='grades')
    subject = models.ForeignKey(Subject, related_name='grades')
    date_started = models.DateField()
    results = models.ForeignKey(SubjectResults, related_name='grades', blank=True, null=True)
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
        year_started = self.date_started.year
        slug_temp = str(self.student) + ' ' +str(self.subject)
        self.slug = slugify(slug_temp)
        super(Grade, self).save() 
