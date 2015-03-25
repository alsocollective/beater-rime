from django.conf.urls import patterns, url

urlpatterns = patterns('timetrack.views',
	url(r'^people', 'people'),
	url(r'^project', 'project'),
	url(r'^stoptimmer', 'stopTimmer'),
	url(r'^starttimmer', 'startTimmer'),
)