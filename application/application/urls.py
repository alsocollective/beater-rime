from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'timetrack.views.home', name='home'),
    url(r'^time/', 'timetrack.views.time', name='home'),    
    url(r'^people/', 'timetrack.views.view_people', name='home'),
    url(r'^project/', 'timetrack.views.view_project', name='home'),
    url(r'^api/',include('timetrack.urls')),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	url(r'^logout/$','django.contrib.auth.views.logout'),

    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
