from django.contrib import admin
from .models import COA, AccountHead, OpeningBalance,BaseCOA

# Register your models here.
admin.site.register(COA)
admin.site.register(AccountHead)
admin.site.register([OpeningBalance,BaseCOA])

