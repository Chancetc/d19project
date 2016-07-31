from django import template

register = template.Library()

@register.filter(name='dic_key')
def dic_key(d,key_name):
	value = ""
	try:
		value = d[key_name]
	except Exception, e:
		value = ""
	return value