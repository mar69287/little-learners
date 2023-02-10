from django.contrib import admin
from .models import Teacher, Guardian, Child

#Register models
admin.site.register(Teacher)
admin.site.register(Guardian)
admin.site.register(Child)
