from django import template

register = template.Library()

@register.filter
def hours(value):

	return int(value/60/60*100)/100.0

