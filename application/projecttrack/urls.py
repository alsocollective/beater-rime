from django.conf.urls import patterns, url

urlpatterns = patterns('projecttrack.views',
	url(r'^project', 'root'),
)