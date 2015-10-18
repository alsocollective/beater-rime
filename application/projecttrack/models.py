import thread,datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# from application.settings import Googlelogin
from timetrack import models as timetrack


class Time_line_event(models.Model):
	class Meta:
		ordering = ['order',]
	name = models.CharField(max_length=500)
	slug = models.SlugField(blank=True)
	description = models.TextField(blank=True, null=True,max_length=2000)
	project = models.ForeignKey('Project')

	order = models.IntegerField(default=0)
	days_offset = models.IntegerField(default=0)
	days_delayed = models.IntegerField(default=0)

	date_due = models.DateField(blank=True, null=True)

	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		super(Time_line_event, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Project(models.Model):
	name = models.CharField(max_length=500)
	slug = models.SlugField(blank=True)

	start_date = models.DateField(blank=True)
	project_time = models.ForeignKey(timetrack.Project)

	notes = models.TextField(blank=True, null=True,max_length=2000)
	
	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		self.update_related_events()
		super(Project, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

	def update_related_events(self):
		if not self.start_date:
			print "no start date given"
			return False
		time_line = Time_line_event.objects.all().filter(project=self)
		off_set = 0
		for event in time_line:
			off_set += self.number_of_days_excluding_weekends(off_set,event.days_offset + event.days_delayed)
			event.date_due = self.start_date + datetime.timedelta(days=off_set-1)
			event.save()


	def number_of_days_excluding_weekends(self,days_start,days_count):
		number_of_non_workdays = 0
		day = 0
		for i in range(days_start,days_start+days_count+1):
			day = (self.start_date + datetime.timedelta(days=i)).weekday()
			if day < 5:
				print "weekday %s"%day
			else:
				number_of_non_workdays += 1
				print "weekend %s"%day

		# check if day is weekend... keep adding till it's not
		if day == 5:
			number_of_non_workdays += 2
		elif day == 6:
			number_of_non_workdays += 1

		return days_count + number_of_non_workdays