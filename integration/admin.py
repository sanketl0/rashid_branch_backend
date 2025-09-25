from django.contrib import admin
from integration.models import *
# Register your models here.
admin.site.register([Task,TaskLogs,VersionHelper])