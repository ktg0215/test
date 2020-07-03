from django import template
from datetime import datetime

register = template.Library() 

@register.filter
def age(v):


    if v is None:
        return None
    else:
        today = datetime.today()
        tyear = today.year
        tmonth= today.month
        tday=today.day
        byear = v.year
        bmonth = v.month
        bday =v.day
        age = tyear-byear
        if tmonth <= bmonth and tday <= bday:
            age = age-1
        return age

 