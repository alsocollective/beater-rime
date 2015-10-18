from django.contrib import admin
from projecttrack import models as project_model


class Time_line_event_inline(admin.TabularInline):
	model = project_model.Time_line_event
	extra = 1
	exclude = ["slug","description"]

class Trello_coloumn_inline(admin.TabularInline):
	model = project_model.Trello_coloumn
	extra = 1
	exclude = ["slug"]

class Project_admin(admin.ModelAdmin):
	# class Media:
	# 	css = {
	# 		'all': ('css/admin/admin.burdock.css',)
	# 	}
	# readonly_fields = ('link_to_invoice','key',)
	# fields = (('client',),'date_invoiced',('paid','fulfilled','date_fulfilled',),'link_to_invoice')#'paying_with_shopify'
	exclude = ["slug",]
	inlines = [
		Time_line_event_inline,
		Trello_coloumn_inline
	]

admin.site.register(project_model.Project,Project_admin)
admin.site.register(project_model.Time_line_event)
admin.site.register(project_model.Trello_coloumn)
