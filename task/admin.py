from django.contrib import admin

# Register your models here.
from task.models import Tasks


admin.site.register(Tasks)
