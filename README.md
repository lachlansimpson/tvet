Student and Staff Information System
====================================

It's purpose is to track Applications, Students and Staff at a Technical Vocational Education and Training institute. 
Qualifications/Courses, the Subjects/Units within, Assessments Enrolments and each subject's Session details are also modelled.

It was written with a specific institution in mind, and as such has Kiribati specific options. 

About
-----
This software was written for the Technical and Vocational Education and Training (TVET) Project being run from the Ministry of Labour and Human Resource Development in the Government of Kiribati.

The final product was in production at the Kiribati Institute of Technology (KIT).

Installation
------------
This software was written in Django 1.4, and should be installed as a django app.

License
-------
This project is open sourced under [GNU GPL Version 3](http://www.gnu.org/licenses/gpl-3.0.html).

See LICENSE file for a full copy of the license

Author
------
Lachlan Musicman Simpson (c) 2012 - [Twitter](http://twitter.com/#datakid23) [E-mail](mailto://lachlan@constraintworks.com)

Notes
-----
In order to be able to provide a small amount of revision control - enough to prevent low level "adjustment" of marks or attendance records, some models keep records of who was the last person to modify them. The implementation for this was derived from here:
https://code.djangoproject.com/wiki/CookBookNewformsAdminAndUser

TODOs, obvious refactorings and just plain old bad architecture:

 - The results/assessment forms, maybe even the assessment/results model in general
 - last_change_by and penultimate - should probably all be moved into their respective model's save method rather than in their admin methods. Currently in admin methods, which means double code when having outside forms.
 - for some reason the .filter().exclude() on the assessment detail view isn't working.
 - Timetable views are still iffy. 
  -- no days on grid if the timetable doesn't have a Morning 1 session 
