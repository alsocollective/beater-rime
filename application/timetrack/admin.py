from django.contrib import admin
from timetrack.models import *

class workAdmin(admin.ModelAdmin):
	list_display = ('person','project','completed','totalhours','totalhourstext','notes')


admin.site.register(Person)
admin.site.register(Project)
admin.site.register(WorkTypes)
admin.site.register(WorkSession,workAdmin)