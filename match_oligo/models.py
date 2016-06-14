from __future__ import unicode_literals

from django.db import models

class user_input(models.Model):
	reference = models.TextField()
	def __str__(self):
		return '%s' % (self.reference,) 
