from django import template
from covid.models import *
register = template.Library()

@register.filter(name = 'notification')
def notification(obj):
    test  = Testrecord.objects.filter(ReportStatus="Not Processed yet")
    return test

@register.simple_tag()
def notificationcount(*args, **kwargs):
    testcount  = Testrecord.objects.filter(ReportStatus="Not Processed yet").count()
    return testcount