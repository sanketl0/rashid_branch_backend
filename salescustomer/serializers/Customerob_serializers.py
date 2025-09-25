from rest_framework import serializers

from transaction.models import MasterTransaction
from salescustomer.models.Customerob_model import CustomerOB



class CustomerObSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOB
        # fields = ['credit','debit','available_balance','customer_id','company_id','ob_id']
        fields = '__all__'
