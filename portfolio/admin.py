from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(count_model)
admin.site.register(patient)
admin.site.register(scanning_reports)
admin.site.register(patient_brain)
admin.site.register(Body_part)
admin.site.register(Gender)
admin.site.register(pain_type)