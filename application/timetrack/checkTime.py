from django.core.mail import send_mail
from timetrack.models import *

# title = "email from %s" %"test"
# message = "Message: %s From: %s"%("test","test")
def sendMail(user,project):
	title = "Courtesy email - you are still working -_-"
	message = "This is a courtesy email to remind you to sign off the time tracker once you are done working on %s. http://time.alsocollective.com/time/" %project
	send_mail(title,message,"bohdan.anderson@gmail.com" ,["bohdan@alsocollective.com",user], fail_silently=False)

projects = WorkSession.objects.all().filter(completed = False)
for project in projects:
	# print project
	# print project.person.user.email
	# print project.project
	sendMail(project.person.user.email,project.project)

print 
