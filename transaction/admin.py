from django.contrib import admin
from transaction.models import MasterTransaction,Charges,ChargeTransaction,CoaCharges
admin.site.register([MasterTransaction,Charges,ChargeTransaction,CoaCharges])
