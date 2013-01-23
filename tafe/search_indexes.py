import datetime
from haystack import indexes
from tafe.models import Applicant, Student, Staff

class ApplicantIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  first_name = indexes.CharField(model_attr='first_name')    
  surname = indexes.CharField(model_attr='surname')    
  island = indexes.CharField(model_attr='island')    
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
