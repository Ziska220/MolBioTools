from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Name(models.Model):
	name_text = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)
	comments_text = models.TextField()
	def __str__(self):
		return '%s %s %s' % (self.name_text, self.email, self.comments_text) 


