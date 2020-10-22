from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.simple_tag()
def getPartName(parts, index):
    if parts:
        parts[index].name
        return parts[index].name
    return None

@register.simple_tag()
def getUnitImg (unit):
    if unit and unit.img:
       return unit.img.url     
    return "/static/img/no_image_hor.jpg"



