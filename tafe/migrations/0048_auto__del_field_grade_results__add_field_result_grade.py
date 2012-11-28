# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Grade.results'
        db.delete_column('tafe_grade', 'results_id')

        # Adding field 'Result.grade'
        db.add_column('tafe_result', 'grade',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='results', to=orm['tafe.Grade']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Grade.results'
        db.add_column('tafe_grade', 'results',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='grades', null=True, to=orm['tafe.Result'], blank=True),
                      keep_default=False)

        # Deleting field 'Result.grade'
        db.delete_column('tafe_result', 'grade_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tafe.applicant': {
            'Meta': {'object_name': 'Applicant'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'applied_for': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applicants'", 'to': "orm['tafe.Course']"}),
            'date_of_application': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_offer_accepted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_offer_sent': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'disability': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'disability_description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'education_level': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'eligibility': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'experience': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': "'1'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'island': ('django.db.models.fields.CharField', [], {'default': "'Tarawa'", 'max_length': "'10'", 'null': 'True', 'blank': 'True'}),
            'last_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'applicant_last_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'other_courses': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'penultimate_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'applicant_penultimate_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'ranking': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_listed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'blank': 'True'}),
            'successful': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'test_ap': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'test_eng': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'test_ma': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tafe.assessment': {
            'Meta': {'object_name': 'Assessment'},
            'date_due': ('django.db.models.fields.DateField', [], {}),
            'date_given': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assessments'", 'to': "orm['tafe.Subject']"})
        },
        'tafe.course': {
            'Meta': {'object_name': 'Course'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Student']", 'null': 'True', 'through': "orm['tafe.Enrolment']", 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'course'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['tafe.Subject']"}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'tafe.credential': {
            'Meta': {'object_name': 'Credential'},
            'aqf_level': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'last_change_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credential_last_change_by'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'penultimate_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'credential_penultimate_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'tafe.enrolment': {
            'Meta': {'object_name': 'Enrolment'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrolments'", 'to': "orm['tafe.Course']"}),
            'date_ended': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 11, 28, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enrolment_last_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'mark': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'penultimate_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enrolment_penultimate_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrolments'", 'to': "orm['tafe.Student']"}),
            'withdrawal_reason': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'})
        },
        'tafe.grade': {
            'Meta': {'object_name': 'Grade'},
            'date_started': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'grade_last_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'penultimate_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'grade_penultimate_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grades'", 'to': "orm['tafe.Student']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grades'", 'to': "orm['tafe.Subject']"})
        },
        'tafe.result': {
            'Meta': {'object_name': 'Result'},
            'assessment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'result'", 'to': "orm['tafe.Assessment']"}),
            'date_submitted': ('django.db.models.fields.DateField', [], {}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['tafe.Grade']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'result_last_change_by'", 'to': "orm['auth.User']"}),
            'mark': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'penultimate_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'result_penultimate_change_by'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'tafe.session': {
            'Meta': {'object_name': 'Session'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room_number': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'session_number': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Student']", 'null': 'True', 'through': "orm['tafe.StudentAttendance']", 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['tafe.Subject']"}),
            'timetable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['tafe.Timetable']"})
        },
        'tafe.staff': {
            'Meta': {'object_name': 'Staff'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'credential': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'credentials'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['tafe.Credential']"}),
            'disability': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'disability_description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': "'1'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'island': ('django.db.models.fields.CharField', [], {'default': "'Tarawa'", 'max_length': "'10'", 'null': 'True', 'blank': 'True'}),
            'last_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'staff_last_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'penultimate_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'staff_penultimate_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tafe.staffattendance': {
            'Meta': {'object_name': 'StaffAttendance'},
            'absent': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'staffattendance_last_change_by'", 'to': "orm['auth.User']"}),
            'penultimate_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'staffattendance_penultimate_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'staffattendance_attendance_records'", 'to': "orm['tafe.Session']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'staff_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attendance_records'", 'to': "orm['tafe.Staff']"})
        },
        'tafe.staffislpr': {
            'Meta': {'object_name': 'StaffISLPR'},
            'date_tested': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'islpr_listening': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'islpr_overall': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'islpr_reading': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'islpr_speaking': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'islpr_writing': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'staff_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'islpr_record'", 'to': "orm['tafe.Staff']"})
        },
        'tafe.student': {
            'Meta': {'object_name': 'Student'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'application_details': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Applicant']"}),
            'disability': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'disability_description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'education_level': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': "'1'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'island': ('django.db.models.fields.CharField', [], {'default': "'Tarawa'", 'max_length': "'10'", 'null': 'True', 'blank': 'True'}),
            'last_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student_last_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'penultimate_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student_penultimate_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tafe.studentattendance': {
            'Meta': {'object_name': 'StudentAttendance'},
            'absent': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'studentattendance_last_change_by'", 'to': "orm['auth.User']"}),
            'penultimate_change_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'studentattendance_penultimate_change_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'studentattendance_attendance_records'", 'to': "orm['tafe.Session']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attendance_records'", 'to': "orm['tafe.Student']"})
        },
        'tafe.studentislpr': {
            'Meta': {'object_name': 'StudentISLPR'},
            'date_tested': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'islpr_listening': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'islpr_overall': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'islpr_reading': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'islpr_speaking': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'islpr_writing': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'islpr_record'", 'to': "orm['tafe.Student']"})
        },
        'tafe.subject': {
            'Meta': {'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'staff_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Staff']", 'null': 'True', 'blank': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Student']", 'null': 'True', 'through': "orm['tafe.Grade']", 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
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