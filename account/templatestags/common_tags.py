from django import template
register = template.Library()

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)

@register.filter(name='asfloat')
def as_float(value):
  return str(value).replace(",", ".")