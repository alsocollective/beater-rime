from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from timetrack.models import *

import datetime,json,datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
@login_required(login_url='/login/')
def root(request):
	projectID = request.GET.get('id')
	if(projectID != None):
		project = Project.objects.get(pk=int(projectID))

		sessions = WorkSession.objects.all().filter(project=project,completed=True).order_by('-endTime')
		timeCounter = 0
		time = []
		date = sessions[0].startTime.date().month
		total = 0
		for ses in sessions:
			if date != ses.startTime.date().month:
				time.append({"m":date, "t":timeCounter})
				total += timeCounter
				date = ses.startTime.date().month
				timeCounter = 0
			timeCounter += ses.totalhours
		if timeCounter > 0:
			time.append({"m":date, "t":timeCounter})
			total += timeCounter

		return render(request,"project.html",{
			"project":project,
			"worksessions":sessions,
			"active":WorkSession.objects.all().filter(project=project,completed=False),
			"timeMonth":time,
			"timeTotal":total
			});

	return render(request,'optionlist.html',{
		"page":"project",
		"data":Project.objects.all().order_by('name').filter(completed=False),
		"data_complete":Project.objects.all().order_by('name').filter(completed=True),
		})
