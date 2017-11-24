# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
import datetime
from django.contrib import messages
from ..login.models import User
from models import Appntmnt

# Create your views here.
def home(request):
    if 'email' not in request.session:
        return redirect('/')
    user_id = request.session['id'] # More clarity
    now = datetime.datetime.now()
    request.session['now'] = str(now.strftime("%Y-%m-%d")) # formatting now time ??why??
    context = {
        
        # "today_appointment": Appntmnt.objects.all().order_by('date', 'time'),
        # 'today_appointment': Appntmnt.objects.filter(entryTime__range=(00:00:AM,11:59:PM)).order_by('time'),
        'today_appointment': Appntmnt.objects.filter(user_appntmnt = user_id).order_by('date', 'time'),
    }    
    return render(request, 'dashboard/homepage.html', context)

def add(request):
    user_id = request.session['id'] # assignment or what??
    results = Appntmnt.objects.validate(request.POST)
    if results['status'] == True:
        new_appntmnt = Appntmnt.objects.create_appntmnt(request.POST, user_id)
        messages.success(request, 'New appointment has been created!')
    else:
        for error in results['errors']:
            messages.error(request, error)    
    return redirect('/dashboard')

def delete(request, id):
    user_id = request.session['id']
    delete = Appntmnt.objects.filter(id = id).delete()
    return redirect('/dashboard')

def edit(request, appntmnt_id):
    if 'email' not in request.session:
        return redirect('/')
    context = {
        "editorial": Appntmnt.objects.filter(id = appntmnt_id)
    }
    request.session['appntmnt'] = appntmnt_id
    return render(request, 'dashboard/edit.html', context)

def update(request, appntmnt_id):
    results = Appntmnt.objects.validate(request.POST)
    if results['status'] == True:
        update_appntmnt = Appntmnt.objects.get(id = appntmnt_id)
        update_appntmnt.task = request.POST['task']
        update_appntmnt.status = request.POST['status']
        update_appntmnt.date = request.POST['date']
        update_appntmnt.time = request.POST['time']
        update_appntmnt.save()
        messages.success(request, 'Your appointment is now up-to-date!')
        return redirect('/dashboard')
    else:
        for error in results['errors']:
            messages.error(request, error)
    return redirect('/dashboard/{}/edit'.format(appntmnt_id))



    

    
   
