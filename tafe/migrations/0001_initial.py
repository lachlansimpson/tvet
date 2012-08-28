# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Student'
        db.create_table('tafe_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(default='F', max_length='1')),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('tafe', ['Student'])

        # Adding model 'Staff'
        db.create_table('tafe_staff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(default='F', max_length='1')),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('tafe', ['Staff'])

        # Adding model 'Subject'
        db.create_table('tafe_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('semester', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('tafe', ['Subject'])

        # Adding model 'Course'
        db.create_table('tafe_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal('tafe', ['Course'])

        # Adding M2M table for field subjects on 'Course'
        db.create_table('tafe_course_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['tafe.course'], null=False)),
            ('subject', models.ForeignKey(orm['tafe.subject'], null=False))
        ))
        db.create_unique('tafe_course_subjects', ['course_id', 'subject_id'])

        # Adding model 'SubjectResults'
        db.create_table('tafe_subjectresults', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('mark', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('tafe', ['SubjectResults'])

        # Adding model 'Attendance'
        db.create_table('tafe_attendance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('reason', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
        ))
        db.send_create_signal('tafe', ['Attendance'])

        # Adding model 'Enrolment'
        db.create_table('tafe_enrolment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tafe.Student'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tafe.Course'])),
            ('date_started', self.gf('django.db.models.fields.DateField')()),
            ('date_ended', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('mark', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
        ))
        db.send_create_signal('tafe', ['Enrolment'])

        # Adding model 'Grade'
        db.create_table('tafe_grade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tafe.Student'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tafe.Subject'])),
            ('date_started', self.gf('django.db.models.fields.DateField')()),
            ('results', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tafe.SubjectResults'], null=True, blank=True)),
        ))
        db.send_create_signal('tafe', ['Grade'])

        # Adding M2M table for field attendance on 'Grade'
        db.create_table('tafe_grade_attendance', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('grade', models.ForeignKey(orm['tafe.grade'], null=False)),
            ('attendance', models.ForeignKey(orm['tafe.attendance'], null=False))
        ))
        db.create_unique('tafe_grade_attendance', ['grade_id', 'attendance_id'])


    def backwards(self, orm):
        # Deleting model 'Student'
        db.delete_table('tafe_student')

        # Deleting model 'Staff'
        db.delete_table('tafe_staff')

        # Deleting model 'Subject'
        db.delete_table('tafe_subject')

        # Deleting model 'Course'
        db.delete_table('tafe_course')

        # Removing M2M table for field subjects on 'Course'
        db.delete_table('tafe_course_subjects')

        # Deleting model 'SubjectResults'
        db.delete_table('tafe_subjectresults')

        # Deleting model 'Attendance'
        db.delete_table('tafe_attendance')

        # Deleting model 'Enrolment'
        db.delete_table('tafe_enrolment')

        # Deleting model 'Grade'
        db.delete_table('tafe_grade')

        # Removing M2M table for field attendance on 'Grade'
        db.delete_table('tafe_grade_attendance')


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
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
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
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.Student']"})
        },
        'tafe.grade': {
            'Meta': {'object_name': 'Grade'},
            'attendance': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Attendance']", 'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'results': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tafe.SubjectResults']", 'null': 'True', 'blank': 'True'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tafe.subject': {
            'Meta': {'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tafe.Student']", 'null': 'True', 'through': "orm['tafe.Grade']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
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