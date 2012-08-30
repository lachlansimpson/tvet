# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Course.slug'
        db.alter_column('tafe_course', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=40))
        # Adding index on 'Course', fields ['slug']
        db.create_index('tafe_course', ['slug'])


        # Changing field 'Subject.slug'
        db.alter_column('tafe_subject', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=40))
        # Adding index on 'Subject', fields ['slug']
        db.create_index('tafe_subject', ['slug'])


        # Changing field 'Student.slug'
        db.alter_column('tafe_student', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=40))
        # Adding field 'Grade.slug'
        db.add_column('tafe_grade', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default=datetime.datetime(2012, 8, 30, 0, 0), max_length=60),
                      keep_default=False)

        # Adding field 'Enrolment.slug'
        db.add_column('tafe_enrolment', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=40, blank=True),
                      keep_default=False)


        # Changing field 'Staff.slug'
        db.alter_column('tafe_staff', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=40))

    def backwards(self, orm):
        # Removing index on 'Subject', fields ['slug']
        db.delete_index('tafe_subject', ['slug'])

        # Removing index on 'Course', fields ['slug']
        db.delete_index('tafe_course', ['slug'])


        # Changing field 'Course.slug'
        db.alter_column('tafe_course', 'slug', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'Subject.slug'
        db.alter_column('tafe_subject', 'slug', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'Student.slug'
        db.alter_column('tafe_student', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))
        # Deleting field 'Grade.slug'
        db.delete_column('tafe_grade', 'slug')

        # Deleting field 'Enrolment.slug'
        db.delete_column('tafe_enrolment', 'slug')


        # Changing field 'Staff.slug'
        db.alter_column('tafe_staff', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

    models = {
        'tafe.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'tafe.course': {
            'Meta': {'object_name': 'Course'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Student']", 'null': 'True', 'through': "orm['tafe.Enrolment']", 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Subject']", 'null': 'True', 'blank': 'True'})
        },
        'tafe.enrolment': {
            'Meta': {'object_name': 'Enrolment'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Course']"}),
            'date_ended': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Student']"})
        },
        'tafe.grade': {
            'Meta': {'object_name': 'Grade'},
            'attendance': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Attendance']", 'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'results': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.SubjectResults']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Student']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Subject']"})
        },
        'tafe.staff': {
            'Meta': {'object_name': 'Staff'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': "'1'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tafe.student': {
            'Meta': {'object_name': 'Student'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': "'1'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tafe.subject': {
            'Meta': {'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Student']", 'null': 'True', 'through': "orm['tafe.Grade']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'tafe.subjectresults': {
            'Meta': {'object_name': 'SubjectResults'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['tafe']