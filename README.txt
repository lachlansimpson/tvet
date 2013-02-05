README

Notes: in order to be able to provide a small amount of revision control - enough to prevent low level "adjustment" of marks or attendance records, some models keep records of who was the last person to modify them. The implementation for this was derived from here:
https://code.djangoproject.com/wiki/CookBookNewformsAdminAndUser

TODOs, obvious refactorings and just plain old bad architecture:

 - The results/assessment forms, maybe even the assessment/results model in general
 - last_change_by and penultimate - should probably all be moved into their respective model's save method rather than in their admin methods. Currently in admin methods, which means double code when having outside forms.
 - for some reason the .filter().exclude() on the assessment detail view isn't working.
