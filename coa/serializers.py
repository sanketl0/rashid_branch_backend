from rest_framework import serializers
from .models import COA, AccountHead,Tax, OpeningBalance,TransactionDetail,TransactionDetailCV,OpeningBalanceView
#import * indicates that is importing model from respective app
from accounting.models import JournalTransaction
from salescustomer.models import *#CreditNoteTransaction, InvoiceJournalTransaction, PaymentTransaction
from purchase.models import *#BillJournalTransaction, PaymentmadeJournalTransaction, DebitNoteTransaction, ExpenseJournalTransaction
from banking.models import *
from banking.serializers import *
from report.models import AccountBalance
###################### Chart of account view ##############################
#Journal Transaction serializer

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['label'] = instance.name
        ret['value'] = instance.rate
        return ret

class JournalTransactionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = JournalTransaction
        fields = '__all__'
        depth=1



#serializer to show selected field in coa table after join 
class OBalanceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = OpeningBalance
        fields = ['opening_balance','closing_balance','debit','credit','coa_id','ob_id', 'migration_date', 'notes']


#this serializer returns all records of Invoicejournal transaction, journal transaction, credit note journal transaction, payment receive journal transaction
class transactionsSerializer(serializers.ModelSerializer):
    # invoice_coa=InvoiceJTSerializer(many=True)
    # jt_coa=JournalTransactionSerializer(many=True)
    # pr_coa=PaymentJTSerializer(many=True)
    # cn_coa=CreditnoteJTSerializer(many=True)
    # # bill_coa=BillJTSerializer(many=True)
    # er_coa=ExpenseJTSerializer(many=True)
    # pm_coa=PaymentmadeJTSerializer(many=True)
    # dn_coa=DebitnoteJTSerializer(many=True)
    # ttaa_coa=TTAATransctionSerializer(many=True)
    # cardpayment_coa=CardPaymentTransactionSerializer(many=True)
    # coa_ownerwithdraw=OwnerdrawingTransactionSerializer(many=True)
    # dtoa_coa=DTOATransactionSerializer(many=True)
    # coa_tfaadata=TFAATransactionSerializer(many=True)
    # coa_interestincome=InterestIncomeTransactionSerlizer(many=True)
    # coa_otherincome=OITSerializer (many=True)
    # coa_exp=ExpRefundTransactionSerializer(many=True)
    # dfoa_coa=DFOATransactionSerializer(many=True)
    # coa_ownerscontribution=OwnersContributionTransactionSerializer(many=True)
    # coa_advancedvendor=VendorAdvancedTransactionSerializer(many=True, read_only=True)
    # coa_vendorpayment=VendorPaymentTransSerializer(many=True, read_only=True)
    # coa_ca=CustomerAdvancedTransctionSerializer(many=True)
    # #coa_cp=CustomerPaymentTransactionSerializer(many=True)
    # # pr_coa=COACustomerPaymentSerializer(many=True)
    # coa_vendorpaymentref=VendorPaymentRefTransSerializer(many=True, read_only=True)
    # coa_debitnoteref=DNRTSerializer(many=True, read_only=True)
    # coa_expbank=ExpbankjtSerializer(many=True, read_only=True)
    # coa_creditnoterefund=CNRTSerializer(many=True, read_only=True)
    # coa_paymentref=PaymentRefundTransctionSerializer(many=True)
    opbalance = OBalanceSerializer(many=True)
    class Meta:
        model = COA
        fields = '__all__'
##############################################################################################
#COA
class COASerializer(serializers.ModelSerializer):
    class Meta:
        model = COA
        fields = '__all__'

#get coa by account name
class accountnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBalance
        fields ='__all__'


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = '__all__'

class TransactionDetailCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetailCV
        fields = '__all__'


class COAopbalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = COA
        fields = ['coa_id','account_type','account_name','account_subhead']
        #fields = '__all__'

#ob serializer
class ObSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningBalance
        fields = ['ob_id','coa_id','closing_balance','opening_balance']
        #fields = '__all__'

#AccountHead
class AccountHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHead
        fields = '__all__'

#OpeningBalance
class OpeningBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningBalance
        fields = ['coa_id','ob_id','opening_balance','closing_balance','available_balance','debit','credit']


#join COA and OB 
class JoinCOASerializer(serializers.ModelSerializer):

    class Meta:
        model = OpeningBalanceView
        fields = '__all__'


# COA serializer short by company (v)
class COASerializerShortbyCompany(serializers.ModelSerializer):
    class Meta:
        model = AccountBalance
        fields ='__all__'


