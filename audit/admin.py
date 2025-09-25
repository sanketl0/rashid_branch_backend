from django.contrib import admin
from audit.models import *
# Register your models here.
admin.site.register(
    [Audit]
)