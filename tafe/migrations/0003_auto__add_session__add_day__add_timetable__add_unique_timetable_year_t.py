# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Session'
        db.create_table('tafe_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_number', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tafe.Subject'])),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tafe.Day'])),
            ('timetable', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tafe.Timetable'])),
        ))
        db.send_create_signal('tafe', ['Session'])

        # Adding model 'Day'
        db.create_table('tafe_day', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('tafe', ['Day'])

        # Adding model 'Timetable'
        db.create_table('tafe_timetable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('term', self.gf('django.db.models.fields.IntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=12)),
        ))
        db.send_create_signal('tafe', ['Timetable'])

        # Adding unique constraint on 'Timetable', fields ['year', 'term']
        db.create_unique('tafe_timetable', ['year', 'term'])

        # Deleting field 'Attendance.date'
        db.delete_column('tafe_attendance', 'date')

        # Deleting field 'Attendance.session'
        db.delete_column('tafe_attendance', 'session')

        # Adding field 'Attendance.absent'
        db.add_column('tafe_attendance', 'absent',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True),
                      keep_default=False)

        # Adding M2M table for field session on 'Attendance'
        db.create_table('tafe_attendance_session', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('attendance', models.ForeignKey(orm['tafe.attendance'], null=False)),
            ('session', models.ForeignKey(orm['tafe.session'], null=False))
        ))
        db.create_unique('tafe_attendance_session', ['attendance_id', 'session_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Timetable', fields ['year', 'term']
        db.delete_unique('tafe_timetable', ['year', 'term'])

        # Deleting model 'Session'
        db.delete_table('tafe_session')

        # Deleting model 'Day'
        db.delete_table('tafe_day')

        # Deleting model 'Timetable'
        db.delete_table('tafe_timetable')

        # Adding field 'Attendance.date'
        db.add_column('tafe_attendance', 'date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 8, 31, 0, 0)),
                      keep_default=False)

        # Adding field 'Attendance.session'
        db.add_column('tafe_attendance', 'session',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2012, 8, 31, 0, 0), max_length=1),
                      keep_default=False)

        # Deleting field 'Attendance.absent'
        db.delete_column('tafe_attendance', 'absent')

        # Removing M2M table for field session on 'Attendance'
        db.delete_table('tafe_attendance_session')


    models = {
        'tafe.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'absent': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'session': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tafe.Session']", 'symmetrical': 'False'})
        },
        'tafe.course': {
            'Meta': {'object_name': 'Course'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Student']", 'null': 'True', 'through': "orm['tafe.Enrolment']", 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Subject']", 'null': 'True', 'blank': 'True'})
        },
        'tafe.day': {
            'Meta': {'object_name': 'Day'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        'tafe.session': {
            'Meta': {'object_name': 'Session'},
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Day']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_number': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Subject']"}),
            'timetable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Timetable']"})
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