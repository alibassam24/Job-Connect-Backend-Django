from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(EmployeeProfile)
admin.site.register(EmployerProfile)
admin.site.register(Experience)
admin.site.register(Job)
admin.site.register(Skills)
admin.site.register(Application)
