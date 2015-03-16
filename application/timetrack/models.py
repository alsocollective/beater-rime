from django.db import models
from django.template.defaultfilters import slugify
import gspread,thread
from application.settings import Googlelogin


def getWorkSheet(pageName):
	gc = gspread.login(Googlelogin["user"], Googlelogin["password"])
	sh = gc.open("timetrackdjango")
	try:
		return sh.worksheet(pageName)
	except Exception, e:
		return sh.add_worksheet(title=pageName, rows="20", cols="10")



class Person(models.Model):
	name = models.CharField(max_length=500)
	slug = models.SlugField(blank=True)

	lastProject = models.ForeignKey("Project",blank=True,null=True)

	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		self.generatePersonPage()
		super(Person, self).save(*args, **kwargs)
	
	def generatePersonPage(self):
		def update():
			persons = Person.objects.all()
			wks = getWorkSheet("People")
			count = len(persons)
			cell_list = wks.range('A1:C%d'%count)
			for i in range(0,count):
				cell_list[(i*3)].value = persons[i]
				worksession = WorkSession.objects.all().filter(person=persons[i],completed=False)
				if(worksession):
					worksession = worksession[0]
					cell_list[(i*3)+1].value=worksession.startTimeFloat
					cell_list[(i*3)+2].value=worksession.project.name
				else:
					cell_list[(i*3)+1].value=0
					cell_list[(i*3)+2].value=0
			wks.update_cells(cell_list)

		thread.start_new_thread(update,())

	def __unicode__(self):
		return self.name

class Project(models.Model):
	name = models.CharField(max_length=500)
	completed = models.BooleanField(default=False)
	slug = models.SlugField(blank=True)

	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		self.generateProjectPage()
		super(Project, self).save(*args, **kwargs)

	def generateProjectPage(self):
		def update(self):
			print "\n\n\n\n\n\n\n\n\n%s\n\n\n\n\n\n\n"%self.name
			wks = getWorkSheet(self.name)
			worksession = WorkSession.objects.all().filter(project=self)
			count = len(worksession)
			cell_list = wks.range('A1:D%d'%count)
			for i in range(0,count):
				cell_list[(i*4)].value = worksession[i].person
				cell_list[(i*4)+1].value=worksession[i].startTimeFloat
				cell_list[(i*4)+2].value=worksession[i].endTimeFloat
				cell_list[(i*4)+3].value="=C%d-B%d"%(i+1,i+1)
			wks.update_cells(cell_list)

		thread.start_new_thread(update,(self,))
	
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

	totalhours = models.FloatField(blank=True, null=True)

	def save(self,*args, **kwargs):
		self.project.generateProjectPage()

	def __unicode__(self):
		return "%s -- %s"%(self.person,self.project)



