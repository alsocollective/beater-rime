from django.db import models
from django.template.defaultfilters import slugify
import gspread,thread,datetime
from application.settings import Googlelogin
from django.contrib.auth.models import User

def println(text):
	print "\n\t%s\n"%text

class Person(models.Model):
	name = models.CharField(max_length=500)
	slug = models.SlugField(blank=True)
	user = models.OneToOneField(User,blank=True,null=True)

	lastProject = models.ForeignKey("Project",blank=True,null=True)

	active = models.BooleanField(default=True)

	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		super(Person, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.name

class Project(models.Model):
	name = models.CharField(max_length=500)
	completed = models.BooleanField(default=False)
	slug = models.SlugField(blank=True)
	notes  = models.TextField(blank=True, null=True,max_length=2000)

	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		super(Project, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class WorkTypes(models.Model):
	name = models.CharField(max_length=500)
	short = models.CharField(max_length=500)
	slug = models.SlugField(blank=True)

	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		super(WorkTypes, self).save(*args, **kwargs)
	def __unicode__(self):
		return self.name

class WorkSession(models.Model):
	person = models.ForeignKey(Person)
	project = models.ForeignKey(Project)
	startTime = models.DateTimeField(blank=True, null=True)
	startTimeFloat = models.FloatField(default=0)

	notes = models.TextField(blank=True, null=True,max_length=1000)
	exiting_notes = models.TextField(blank=True, null=True,max_length=2000)

	endTime = models.DateTimeField(blank=True, null=True)
	endTimeFloat = models.FloatField(default=0)

	completed = models.BooleanField(default=False)

	minusTime = models.FloatField(default=0)
	pauseStart = models.FloatField(blank=True, null=True)
	pauseEnd = models.FloatField(blank=True, null=True)

	# should be called totalseconds
	totalhours = models.FloatField(blank=True, null=True)
	totalhourstext = models.CharField(max_length=200,blank=True,null=True)

	workTypes = models.ForeignKey(WorkTypes,blank=True,null=True)

	def save(self,*args, **kwargs):
		if self.completed:
			self.deltaTime()
		else:
			self.startTime = datetime.datetime.fromtimestamp(self.startTimeFloat)
		super(WorkSession, self).save(*args, **kwargs)

	def deltaTime(self):
		t1 = datetime.datetime.fromtimestamp(self.startTimeFloat)
		t2 = datetime.datetime.fromtimestamp(self.endTimeFloat)
		self.endTime = t2
		delta = t2-t1
		self.totalhours = delta.total_seconds()-self.minusTime
		self.totalhourstext = str(delta)

	def pauseLength(self):
		t1 = datetime.datetime.fromtimestamp(self.pauseStart)
		t2 = datetime.datetime.fromtimestamp(self.pauseEnd)
		delta = t2-t1
		self.pauseStart = 0
		self.pauseEnd = 0
		self.minusTime += delta.total_seconds()
		self.save()


	def __unicode__(self):
		return "%s -- %s"%(self.person,self.project)



