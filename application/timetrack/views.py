from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from timetrack.models import *

import datetime,json,datetime


def home(request):
	return render(request,'index.html',{"users":Person.objects.all(),"projects":Project.objects.all(),"worksession":WorkSession.objects.all()})

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
			data["pause"]=worksession.pauseStart
			data["delay"]=worksession.minusTime
		out.append(data)
	return HttpResponse(json.dumps(out), content_type="application/json")

def project(request):
	out = []
	for project in Project.objects.all():
		out.append({"name":project.name,"pk":project.pk})
	return HttpResponse(json.dumps(out), content_type="application/json")


def stopTimmer(request):
	pause = request.POST.get('pause')
	name = request.POST.get('name')
	person = Person.objects.get(pk=name);

	projectsOnTheGo = WorkSession.objects.all().filter(person=person,completed=False)
	if(not projectsOnTheGo):
		return render(request,'error.html',{"error":"%s's not on a project"%person})
	projectsOnTheGo = projectsOnTheGo[0]

	if pause:
		print "\n\n%s"%"pause"
		if projectsOnTheGo.pauseStart:
			print "\tpauseend"
			projectsOnTheGo.pauseEnd = float(request.POST.get('time'))
			projectsOnTheGo.pauseLength()
		else:
			print "\tpausestart"			
			projectsOnTheGo.pauseStart = float(request.POST.get('time'))
			projectsOnTheGo.save()
		return redirect("/")

	projectsOnTheGo.endTimeFloat = float(request.POST.get('time'))

	if projectsOnTheGo.pauseStart:
		projectsOnTheGo.pauseEnd = projectsOnTheGo.endTimeFloat
		projectsOnTheGo.pauseLength()

	projectsOnTheGo.completed = True
	projectsOnTheGo.save()

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
	project = Project.objects.get(pk=request.POST.get('project'))
	message = request.POST.get('task')
	time = float(request.POST.get('time'))
	workType = request.POST.get('worktype')

	if not workType:
		workType = ""

	w = WorkSession(
		person=person,
		project=project,
		startTimeFloat=time,
		notes=message,
		workType=workType
		)
	w.save()

	person.generatePersonPage()
	return redirect("/")

def view_people(request):
	return HttpResponse("people");
	
def view_project(request):
	return HttpResponse("projects");