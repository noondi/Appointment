# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    # validation and filtering errors
    def validate(self, postData):
        results = {           
            'status': True, 
            'errors': []
            }
        # name validation
        if len(postData['name']) < 3:
            results['errors'].append('Your name is too short.')
            results['status'] = False
        if not re.match("^[a-zA-Z ]*$", postData['name']):
            results['errors'].append('Name cannot contain numbers or special characters')
            results['status'] = False
        # email validation
        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            results['errors'].append('Email is not valid')
            results['status'] = False
        if len(self.filter(email = postData['email'])) > 0:
            results['errors'].append('Email entered is already registered.') # Checking if the entered email exists!!
            results['status'] = False
        # password validation
        if len(postData['password']) < 8:
            results['errors'].append('Password is too short')
            results['status'] = False
        if postData['password'] != postData['cnfpw']:
            results['errors'].append('Passwords do not match')
            results['status'] = False
        # birthdate validation
        now = datetime.datetime.now()
        bday = datetime.datetime.strptime(
            postData['bday'], 
            '%Y-%m-%d'
            )
        if bday > now:   # checking if birthdate if beyond Today!!!
            results['errors'].append("You cannot be born in the future!")
            results['status'] = False
        return results
    #creating the user
    def creator(self, postData):
        user = self.create(
            name = postData['name'],
            email = postData['email'],
            password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()),
            bday = postData['bday'])
        return user  
    # logging the user in .....
    def loginVal(self, postData):
        results = {
            'status': True, 
            'errors': [], 
            'user': None,
            }
        users = self.filter(
            email = postData['email']
            )
        if len(users) < 1:
            results['status'] = False
        else:
            if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                results['user'] = users[0]
            else:
                results['status'] = False
        return results   
        
class User(models.Model):
    name = models.CharField(max_length =255)
    email = models.CharField(max_length =255)
    password = models.CharField(max_length =255)
    bday = models.DateField(auto_now=False, auto_now_add=False) # ???!! auto_now issues!!
    objects = UserManager()
