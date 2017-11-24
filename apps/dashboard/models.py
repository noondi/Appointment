# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login.models import User
from django.db import models
import datetime
import re

# Create your models here.
class AppntmntManager(models.Manager):
    def validate(self, postData):
        results = {
            'status': True,
            'errors': []
            }
        # field validation
        if len(postData['task']) < 1:
            results['errors'].append('Task field cannot be empty')
            results['status'] = False

        # current or future dates     
        now = datetime.datetime.now()
        date = datetime.datetime.strptime(
            postData['date'], 
            '%Y-%m-%d'
            )
        if date < now:   # checking if date is before today!!!
            results['errors'].append("You cannot set an appointment in the past!")
            results['status'] = False 
        return results

    def create_appntmnt(self, postData, user_id):       
        new_appntmnt = self.create( # logged_in user creates appntmnt 
            date = postData['date'], 
            time = postData['time'],
            task = postData['task'], 
            status = 'pending', # user sets appntmnt to pending
            user_appntmnt = User.objects.get(id = user_id)) # more here??!!
        return new_appntmnt

class Appntmnt(models.Model):
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    date = models.CharField(max_length =255)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    user_appntmnt = models.ForeignKey(User, related_name="appntmnts")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = AppntmntManager()

    def __repr__(self):
        return "<Appntmnt object: {} {}>".format(self.task, self.status, self.time, self.user_appntmnt)

       
        



