from django.contrib import admin
from .models import Company, Branch, FinancialYear,Company_Year,Defaults

# Register your models here.
admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(FinancialYear)
admin.site.register(Company_Year)
admin.site.register(Defaults)