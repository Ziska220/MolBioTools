from django.db import models

import datetime
from django.utils import timezone

class user_input(models.Model):
    reference = models.TextField()
    def __str__(self):
        return '%s' % (self.reference,)