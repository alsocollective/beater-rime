from django.db import models
from django.template.defaultfilters import slugify
import gspread,thread,datetime
from application.settings import Googlelogin

def println(text):
	print "\n\t%s\n"%text

def getWorkSheet(pageName):
	gc = gspread.login(Googlelogin["user"], Googlelogin["password"])
	# retrive active spreadsheet
	try:
		sheet = SpreadSheet.objects.get(active=True).name
	except Exception, e:
		print e
		sheet = "testtimer"

	sh = gc.open(sheet)
	try:
		return sh.worksheet(pageName)
	except Exception, e:
		return sh.add_worksheet(title=pageName, rows="200", cols="9")

#creates a page with content feed into it
#page name 			= "page to be generate"
#content 			= array of elements to be parsed
#parseArrayFunction	= function returns an array of elements to be saved the same size as coloumns
#coloumns 			= the number of elements to be returned by parseArrayFunction
def generatePage(pageName,content,parseArrayFunction,coloumns):
	print "\t generating: %s page"%pageName
	wks = getWorkSheet(pageName)
	count = len(content)
	cell_list = wks.range('A2:%s%d'%(chr(64+coloumns),count+1))
	for i in range(0,count):
		data = parseArrayFunction(content[i])
		for x in range(0,coloumns):
			cell_list[(i*coloumns)+x].value = data[x]
	wks.update_cells(cell_list)
	print "\t generated: %s page"%pageName

class SpreadSheet(models.Model):
	name = models.CharField(max_length=1000)
	slug = models.SlugField(blank=True)
	active = models.BooleanField(default=False)
	url = models.CharField(max_length=2000,blank=True)

	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		self.getURL()
		super(SpreadSheet, self).save(*args, **kwargs)

	def getURL(self):
		gc = gspread.login(Googlelogin["user"], Googlelogin["password"])
		sh = gc.open(self.name)
		self.url = "https://docs.google.com/a/alsocollective.com/spreadsheets/d/%s"%sh.id

	def __unicode__(self):
		return self.name

class Person(models.Model):
	name = models.CharField(max_length=500)
	slug = models.SlugField(blank=True)

	sheet = models.ForeignKey(SpreadSheet,blank=True,null=True)
	lastProject = models.ForeignKey("Project",blank=True,null=True)

	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		self.generatePersonPage()
		self.setSheet()
		super(Person, self).save(*args, **kwargs)
	
	def setSheet(self):
		try:
			self.sheet = SpreadSheet.objects.get(active=True)
		except Exception, e:
			print e

	def generatePersonPage(self):
		content = Person.objects.all()
		def parser(person):
			worksession = WorkSession.objects.all().filter(person=person,completed=False)
			if worksession:
				worksession = worksession[0]
				return [person,worksession.startTime,worksession.project.name,worksession.notes]
			return [person,"","",""]
		thread.start_new_thread(generatePage,("People",content,parser,4))


		contentPerson = WorkSession.objects.all().filter(person=self)
		def personParser(task):
			return [
				task.project,
				task.startTime,
				task.notes,
				task.workTypes,
				task.totalhours,
				task.minusTime
			]

		thread.start_new_thread(generatePage,(self.name,contentPerson,personParser,6))


	def __unicode__(self):
		return self.name

class Project(models.Model):
	name = models.CharField(max_length=500)
	completed = models.BooleanField(default=False)
	slug = models.SlugField(blank=True)
	sheet = models.ForeignKey(SpreadSheet,blank=True,null=True)

	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		self.generateProjectPage()
		self.setSheet()
		super(Project, self).save(*args, **kwargs)

	def setSheet(self):
		try:
			self.sheet = SpreadSheet.objects.get(active=True)
		except Exception, e:
			print e

	def generateProjectPage(self):
		content = WorkSession.objects.all().filter(project=self)
		def parser(element):
			return [element.person,element.startTime,element.endTime,element.totalhours,element.totalhourstext,element.workTypes,element.notes]
		thread.start_new_thread(generatePage,(self.name,content,parser,7))
	
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

	endTime = models.DateTimeField(blank=True, null=True)
	endTimeFloat = models.FloatField(default=0)

	completed = models.BooleanField(default=False)

	minusTime = models.FloatField(default=0)
	pauseStart = models.FloatField(blank=True, null=True)
	pauseEnd = models.FloatField(blank=True, null=True)

	# should be called totalseconds
	totalhours = models.FloatField(blank=True, null=True)
	totalhourstext = models.CharField(max_length=200,blank=True,null=True)

	#workType
	# WORK_CHOISES = [
	# 	("design","design"),
	# 	("development","development"),
	# 	("email","email"),
	# 	("spagetti","spagetti"),
	# 	("admin","admin")]
	# workType = models.CharField(max_length=12, choices=WORK_CHOISES, default='')

	workTypes = models.ForeignKey(WorkTypes,blank=True,null=True)

	sheet = models.ForeignKey(SpreadSheet,blank=True,null=True)

	def save(self,*args, **kwargs):
		if self.completed:
			self.deltaTime()
			self.project.generateProjectPage()
		else:
			self.startTime = datetime.datetime.fromtimestamp(self.startTimeFloat)
		self.setSheet()		
		super(WorkSession, self).save(*args, **kwargs)

	def setSheet(self):
		try:
			self.sheet = SpreadSheet.objects.get(active=True)
		except Exception, e:
			print e

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



