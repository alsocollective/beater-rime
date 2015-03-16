from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from timetrack.models import *

import datetime,json,datetime


def home(request):
	return render(request,'index.html',{"users":Person.objects.all(),"projects":Project.objects.all()})

def people(request):
	out = []
	for person in Person.objects.all():
		worksession = WorkSession.objects.all().filter(person=person,completed=False)
		data = {"name":person.name,"pk":person.pk}
		if(worksession):
			worksession = worksession[0]
			data["start"]=worksession.startTimeFloat
			data["project"]=worksession.project.name
			data["projectpk"]=worksession.project.pk
		out.append(data)
	return HttpResponse(json.dumps(out), content_type="application/json")

def project(request):
	out = []
	for project in Project.objects.all():
		out.append({"name":project.name,"pk":project.pk})
	return HttpResponse(json.dumps(out), content_type="application/json")


def stopTimmer(request):
	name = request.POST.get('name')
	person = Person.objects.get(pk=name);

	projectsOnTheGo = WorkSession.objects.all().filter(person=person,completed=False)
	if(not projectsOnTheGo):
		return render(request,'error.html',{"error":"%s's not on a project"%person})

	projectsOnTheGo[0].endTimeFloat = request.POST.get('time')
	projectsOnTheGo[0].completed = True
	projectsOnTheGo[0].save()
	person.generatePersonPage()
	return redirect("/")


def startTimmer(request):
	#datetime.datetime.fromtimestamp(float(request.POST.get('time')))

	name = request.POST.get('name')
	person = Person.objects.get(pk=name);

	#test if person is in work session already...
	projectsOnTheGo = WorkSession.objects.all().filter(person=person,completed=False)
	if(projectsOnTheGo):
		return render(request,'error.html',{"error":"%s's already on project"%person})

	#generate new work session
	w = WorkSession(
		person=person,
		project=Project.objects.get(pk=request.POST.get('project')),
		startTimeFloat=float(request.POST.get('time'))
		)
	
	w.save()
	person.generatePersonPage()
	return redirect("/")

