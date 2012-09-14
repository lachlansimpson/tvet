# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Attendance.session'
        db.add_column('tafe_attendance', 'session',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['tafe.Session']),
                      keep_default=False)

        # Adding field 'Attendance.student'
        db.add_column('tafe_attendance', 'student',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['tafe.Student']),
                      keep_default=False)

        # Removing M2M table for field session on 'Attendance'
        db.delete_table('tafe_attendance_session')

        # Removing M2M table for field attendance on 'Grade'
        db.delete_table('tafe_grade_attendance')


    def backwards(self, orm):
        # Deleting field 'Attendance.session'
        db.delete_column('tafe_attendance', 'session_id')

        # Deleting field 'Attendance.student'
        db.delete_column('tafe_attendance', 'student_id')

        # Adding M2M table for field session on 'Attendance'
        db.create_table('tafe_attendance_session', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('attendance', models.ForeignKey(orm['tafe.attendance'], null=False)),
            ('session', models.ForeignKey(orm['tafe.session'], null=False))
        ))
        db.create_unique('tafe_attendance_session', ['attendance_id', 'session_id'])

        # Adding M2M table for field attendance on 'Grade'
        db.create_table('tafe_grade_attendance', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('grade', models.ForeignKey(orm['tafe.grade'], null=False)),
            ('attendance', models.ForeignKey(orm['tafe.attendance'], null=False))
        ))
        db.create_unique('tafe_grade_attendance', ['grade_id', 'attendance_id'])


    models = {
        'tafe.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'absent': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Session']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Student']"})
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
            'date_started': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'results': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.SubjectResults']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Student']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Subject']"})
        },
        'tafe.session': {
            'Meta': {'object_name': 'Session'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_number': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Student']", 'null': 'True', 'through': "orm['tafe.Attendance']", 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Subject']"}),
            'timetable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['tafe.Timetable']"})
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
