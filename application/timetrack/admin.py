from django.contrib import admin
from timetrack.models import *


admin.site.register(Person)
admin.site.register(Project)
admin.site.register(WorkSession)