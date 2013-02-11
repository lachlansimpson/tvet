import datetime
from haystack import indexes
from tafe.models import Applicant, Student, Staff, Enrolment, Grade

class ApplicantIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  first_name = indexes.CharField(model_attr='first_name')    
  surname = indexes.CharField(model_attr='surname')    
  island = indexes.CharField(model_attr='island', null=True)    
  phone = indexes.CharField(model_attr='phone')    
  phone2 = indexes.CharField(model_attr='phone2')    
  email = indexes.CharField(model_attr='email')    
  dob = indexes.DateField(model_attr='dob')    

  def get_model(self):
      return Applicant

  def index_queryset(self):
      return self.get_model().objects.all()

class StudentIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  first_name = indexes.CharField(model_attr='first_name')    
  surname = indexes.CharField(model_attr='surname')    
  island = indexes.CharField(model_attr='island')    
  phone = indexes.CharField(model_attr='phone')    
  phone2 = indexes.CharField(model_attr='phone2')    
  email = indexes.CharField(model_attr='email')    
  dob = indexes.DateField(model_attr='dob')    

  def get_model(self):
      return Student 

  def index_queryset(self):
      return self.get_model().objects.all()

class EnrolmentIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  student = indexes.CharField(model_attr='student')    
  course = indexes.CharField(model_attr='course')    

  def get_model(self):
      return Enrolment 

  def index_queryset(self):
      return self.get_model().objects.all()

  def prepare_student(self, obj):
      return obj.student.__unicode__()

  def prepare_course(self, obj):
      return obj.course.__unicode__()

class GradeIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  student = indexes.CharField(model_attr='student')    
  subject = indexes.CharField(model_attr='subject')    

  def get_model(self):
      return Grade 

  def index_queryset(self):
      return self.get_model().objects.all()

