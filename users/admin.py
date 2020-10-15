from django.contrib import admin
from .models import Profile, WeightRecord, LiftRecord

admin.site.register(Profile)
admin.site.register(WeightRecord)
admin.site.register(LiftRecord)
