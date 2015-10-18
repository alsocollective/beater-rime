from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from timetrack.models import *

import datetime,json,datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout




@login_required(login_url='/login/')
def home(request):

	return render(request,'index.html')

@login_required(login_url='/login/')
def time(request):
	try:
		user = Person.objects.get(user=request.user);
	except Exception, e:
		return render(request,'error.html',{"error":"Users uknown or not loged in, please login","login":True})

	currentProject = WorkSession.objects.all().filter(person=user,completed=False)
	return render(request,'time.html',{
		"user":user,
		"current":currentProject,
		"projects":Project.objects.all().filter(completed=False).order_by('name'),
		"worksession":WorkSession.objects.all(),
		"worktypes":WorkTypes.objects.all()}
		)

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
	# name = request.POST.get('name')
	try:
		person = Person.objects.get(user=request.user);
	except Exception, e:
		return render(request,'error.html',{"error":"Users uknown or not loged in, please login"})

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
			print request.POST.get('time')
			projectsOnTheGo.pauseStart = float(request.POST.get('time'))
			projectsOnTheGo.save()
		return redirect("/time/")

	projectsOnTheGo.endTimeFloat = float(request.POST.get('time'))

	if projectsOnTheGo.pauseStart:
		projectsOnTheGo.pauseEnd = projectsOnTheGo.endTimeFloat
		projectsOnTheGo.pauseLength()

	projectsOnTheGo.exiting_notes = request.POST.get('workingnotes')
	projectsOnTheGo.completed = True
	projectsOnTheGo.save()

	# person.generatePersonPage()
	return redirect("/time/")


def startTimmer(request):
	#datetime.datetime.fromtimestamp(float(request.POST.get('time')))
	# name = request.user.username#request.POST.get('name')
	try:
		person = Person.objects.get(user=request.user);
	except Exception, e:
		return render(request,'error.html',{"error":"Users uknown or not loged in, please login"})

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

	# person.generatePersonPage()
	return redirect("/time/")

@login_required(login_url='/login/')
def view_people(request):
	userID = request.GET.get('id')
	if(userID != None):
		person = Person.objects.get(pk=int(userID))

		return render(request,"person.html",{
			"person":person,
			"worksessions":WorkSession.objects.all().filter(person=person,completed=True).order_by('-endTime'),
			"active":WorkSession.objects.all().filter(person=person,completed=False)
			});

	return render(request,'optionlist.html',{"page":"people","data":Person.objects.all().order_by('name')})

@login_required(login_url='/login/')
def view_project(request):
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

@login_required(login_url='/login/')
def view_edit(request):
	workSessionID = request.GET.get('id')
	isPost = request.POST.get('id')
	print("\n\n==")
	print(isPost)
	if(isPost and workSessionID != None):
		workSession = WorkSession.objects.get(pk=int(workSessionID))
		workSession.startTimeFloat = float(request.POST.get('startTime'))
		workSession.endTimeFloat = float(request.POST.get('endTime'))
		workSession.notes = request.POST.get('notes')
		workSession.exiting_notes = request.POST.get('exiting_notes')
		workSession.save()
		return render(request,"editWorkSession.html",{
			"workSession":workSession,
			"saved":True
			});
	if(workSessionID != None):
		workSession = WorkSession.objects.get(pk=int(workSessionID))

		return render(request,"editWorkSession.html",{
			"workSession":workSession,
			"saved":False
			});

	return render(request,'optionlist.html',{"page":"project","data":Project.objects.all().order_by('name')})
