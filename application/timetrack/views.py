from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from timetrack.models import *

import datetime,json,datetime

from django.contrib.auth.decorators import login_required


def getActiveSheetURL():
	try:
		return SpreadSheet.objects.get(active=True).url
	except Exception, e:
		print e
		return "/"

@login_required(login_url='/login/')
def home(request):
	return render(request,'index.html',{"users":Person.objects.all().order_by('name'),"projects":Project.objects.all().order_by('name'),"worksession":WorkSession.objects.all(),"spreadsheet":getActiveSheetURL(),"worktypes":WorkTypes.objects.all()})

def people(request):
	out = []
	for person in Person.objects.all():
		worksession = WorkSession.objects.all().filter(person=person,completed=False)
		data = {"name":person.name,"pk":person.pk}
		if(worksession):
			worksession = worksession[0]
			data["start"]=worksession.startTimeFloat
			data["project"]=worksession.project.name
			data["notes"]=worksession.notes
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
	print "\n\n\n\n\n!!!!!!!!"
	print workType
	if not workType:
		workType = None
	else:
		workType = WorkTypes.objects.get(slug=workType)
	w = WorkSession(
		person=person,
		project=project,
		startTimeFloat=time,
		notes=message,
		workTypes=workType
		)
	w.save()

	person.generatePersonPage()
	return redirect("/")

@login_required(login_url='/login/')
def view_people(request):
	userID = request.GET.get('id')
	if(userID != None):
		person = Person.objects.get(pk=int(userID))

		return render(request,"person.html",{
			"person":person,
			"worksessions":WorkSession.objects.all().filter(person=person,completed=True).order_by('-endTime'),
			"active":WorkSession.objects.all().filter(person=person,completed=False),
			"spreadsheet":getActiveSheetURL()
			});

	return render(request,'optionlist.html',{"page":"people","data":Person.objects.all().order_by('name'),"spreadsheet":getActiveSheetURL()})

@login_required(login_url='/login/')
def view_project(request):
	projectID = request.GET.get('id')
	if(projectID != None):
		project = Project.objects.get(pk=int(projectID))

		return render(request,"project.html",{
			"project":project,
			"worksessions":WorkSession.objects.all().filter(project=project,completed=True).order_by('-endTime'),
			"active":WorkSession.objects.all().filter(project=project,completed=False),
			"spreadsheet":getActiveSheetURL()
			});

	return render(request,'optionlist.html',{"page":"project","data":Project.objects.all().order_by('name'),"spreadsheet":getActiveSheetURL()})


