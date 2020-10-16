from django.contrib import admin
from .models import Profile, WeightRecord, LiftRecord, LiftRecord2

admin.site.register(Profile)
admin.site.register(WeightRecord)
admin.site.register(LiftRecord)
admin.site.register(LiftRecord2)
