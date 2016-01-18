from django.contrib import admin
from timetrack.models import *



class workAdmin(admin.ModelAdmin):
	list_display = ('person','project','completed','totalhours','totalhourstext','notes')

	def resave(modeladmin, request, queryset):
		# queryset.update(totalhours=0)
		# queryset.save()
		for obj in queryset:
			obj.save()
	resave.short_description = "Resave selected"

	actions = [resave]




admin.site.register(Person)
admin.site.register(Project)
# admin.site.register(SpreadSheet)
admin.site.register(WorkTypes)
admin.site.register(WorkSession,workAdmin)