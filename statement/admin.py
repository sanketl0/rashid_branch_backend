from django.contrib import admin
from statement.models import *
admin.site.register([Bank,FileUpload,Transaction,TransactionDetail])
