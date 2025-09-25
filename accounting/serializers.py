from rest_framework import serializers

from report.serializers import MasterJournalSerializer
from .models import JournalTransaction, ManualJournal, RecJournal, BulkUpdate, Budget

#ManualJournal
class manualjournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualJournal
        fields = '__all__'

#Journal Transaction serializer
class JournalTransactionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = JournalTransaction
        fields = '__all__'
        #depth = 1
        
#join Manual journal and JournalTransaction
class ManualJournalTransSerializer(serializers.ModelSerializer):    
    class Meta:
        model = JournalTransaction        
        fields = ['mj_id','jt_id','customer_id','coa_id','des','debit','credit']
        depth=1

class JoinJournalTransSerializer(serializers.ModelSerializer):    
    class Meta:
        model = ManualJournal
        fields = '__all__'
        depth=1

#short journal
class shortmanualjournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualJournal
        fields = '__all__'

#RecJournal
class RecJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecJournal
        fields = '__all__'

#BulkUpdate
class BulkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkUpdate
        fields = '__all__'

#Budget
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'


# serializer for Adjustment Short View (v)
class JoinJournalTransSerializer(serializers.ModelSerializer):    
    class Meta:
        model = ManualJournal
        fields = ['mj_id', 'journal_serial_no', 'journal_ref_no', 'journal_status', 'sub_total','journal_date']
