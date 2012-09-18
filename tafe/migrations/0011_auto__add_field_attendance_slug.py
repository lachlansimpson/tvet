# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Attendance.slug'
        db.add_column('tafe_attendance', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=50, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Attendance.slug'
        db.delete_column('tafe_attendance', 'slug')


    models = {
        'tafe.applicant': {
            'Meta': {'object_name': 'Applicant'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'applied_for': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applicants'", 'to': "orm['tafe.Course']"}),
            'date_offer_accepted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_offer_sent': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'disability': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disability_description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'education_level': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'eligibility': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': "'1'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'island': ('django.db.models.fields.CharField', [], {'default': "'01'", 'max_length': "'2'", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'ranking': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_listed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'blank': 'True'}),
            'successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'test_ap': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'test_eng': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'test_ma': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tafe.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'absent': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attendance_records'", 'to': "orm['tafe.Session']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attendance_records'", 'to': "orm['tafe.Student']"})
        },
        'tafe.course': {
            'Meta': {'object_name': 'Course'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Student']", 'null': 'True', 'through': "orm['tafe.Enrolment']", 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'courses'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['tafe.Subject']"})
        },
        'tafe.enrolment': {
            'Meta': {'object_name': 'Enrolment'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrolments'", 'to': "orm['tafe.Course']"}),
            'date_ended': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 9, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrolments'", 'to': "orm['tafe.Student']"})
        },
        'tafe.grade': {
            'Meta': {'object_name': 'Grade'},
            'date_started': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'results': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'grades'", 'null': 'True', 'to': "orm['tafe.SubjectResults']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grades'", 'to': "orm['tafe.Student']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grades'", 'to': "orm['tafe.Subject']"})
        },
        'tafe.session': {
            'Meta': {'object_name': 'Session'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_number': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Student']", 'null': 'True', 'through': "orm['tafe.Attendance']", 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['tafe.Subject']"}),
            'timetable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['tafe.Timetable']"})
        },
        'tafe.staff': {
            'Meta': {'object_name': 'Staff'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disability': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disability_description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': "'1'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'island': ('django.db.models.fields.CharField', [], {'default': "'01'", 'max_length': "'2'", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tafe.student': {
            'Meta': {'object_name': 'Student'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disability': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disability_description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'education_level': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': "'1'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'island': ('django.db.models.fields.CharField', [], {'default': "'01'", 'max_length': "'2'", 'null': 'True', 'blank': 'True'}),
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
        },
        'tafe.timetable': {
            'Meta': {'unique_together': "(('year', 'term'),)", 'object_name': 'Timetable'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '12'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'term': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['tafe']