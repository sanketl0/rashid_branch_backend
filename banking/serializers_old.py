from rest_framework import serializers
from banking .models import *
#Banking Serializers
class BankingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banking
        fields='__all__'

# GET Short By Company id
class BankCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Banking
        fields=['coa_id','bank_id','bank_name','account_type','account_name','bank_name','account_code','ifsc_code']


#################################################
# Transfer To Another Account Serializers
class TransferToAnotherAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=TTAA
        fields='__all__' 

#Transfer to Another Account Serializers
class TTAATransctionSerializer(serializers.ModelSerializer):
    class Meta:
        model=TTAATransaction
        fields='__all__' 
        depth=1

# using Get Short By COA ID 
class ChartedAccountTTAASerializer(serializers.ModelSerializer):
    ttaa_coa=TTAATransctionSerializer(many=True)
    class Meta:
        model=COA
        fields=["coa_id",'ttaa_coa']

#######################################################
#Card payment Serializer
class CardPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CardPayment
        fields='__all__'
        depth=1
#Card Payment Transaction Serializer
class CardPaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=CardPaymentTransaction
        fields='__all__'

# using Get Short By COA ID 
class ChartedAccountCardPaymentSerializer(serializers.ModelSerializer):
    coa_cardpayment=CardPaymentTransactionSerializer(many=True)
    class Meta:
        model=COA
        fields=["coa_id",'data_cardpayment']
################################################################
#DTOA Serializer
class DTOASerializer(serializers.ModelSerializer):
    class Meta:
        model=DTOA
        fields='__all__'
#DTOA Transction
class DTOATransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=DTOATransaction
        fields='__all__'
        depth=1
# GET COA By ID Seriallizer DTOA
class ChartedAccountDTOASerializer(serializers.ModelSerializer):
    dtoa_coa=DTOATransactionSerializer(many=True)
    class Meta:
        model=COA
        fields=["coa_id",'dtoa_coa']

#################################################################
#PaymentRefunds Serializer
class PaymentRefundSerializer(serializers.ModelSerializer):
    class Meta:
        model=RefundMaster
        fields='__all__'
#PaymentRefundTransction Serializer
class PaymentRefundTransctionSerializer(serializers.ModelSerializer):
    class Meta:
        model=PaymentRefundsTransaction
        fields='__all__'
        depth=1

#Payment Recived Serializer
class PRSerializer(serializers.ModelSerializer):
    class Meta:
        model=PR
        fields=['payment_serial','amount_received','balance_amount','pr_id','amount_due','amount_excess']
# GET Customer id by 
class PRCustomerSerializer(serializers.ModelSerializer):
    customer_pr=PRSerializer(many=True)
    class Meta:
        model=SalesCustomer
        fields=['customer_pr']

# GET COA By ID Seriallizer Payment Refund
class ChartedAccountPaymentRefundSerializer(serializers.ModelSerializer):
    coa_paymentref=PaymentRefundTransctionSerializer(many=True)
    class Meta:
        model=COA
        fields=["coa_id",'coa_paymentref']

class CustomerAdvSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerAdvance
        fields='__all__'
        depth=1

class CustomerPaymentRefundSerializer(serializers.ModelSerializer):
    customer_ad=serializers.SerializerMethodField('getamount')
    def getamount(self, customer):
        query=CustomerAdvance.objects.filter(balance_amount__gt=0, customer_id=customer)
        serializer=CustomerAdvSerializer(instance=query, many=True)
        return serializer.data
    class Meta:
        model=SalesCustomer
        fields=['customer_ad']

############################################################
# Customer Advanced
class CustomerAdvancedSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerAdvance
        fields='__all__'
        depth=1

#CustomerAdvaanced Transction 
class CustomerAdvancedTransctionSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerAdvanceTransaction
        fields='__all__'
        depth=1
        

# GET COA By ID Seriallizer Customer Advance
class COACustomerAdvancedSerializer(serializers.ModelSerializer):
    coa_ca=CustomerAdvancedTransctionSerializer(many=True)
    class Meta:
        model=COA
        fields=['coa_ca']
##################################################################
#Customer Payment
class CustomerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerPayment
        fields='__all__'

# #CustomerPaymentTransaction
# class CustomerPaymentTransactionSerializer(serializers.ModelSerializer):
#     customer_payment=serializers.SerializerMethodField('getbank_id')
#     def getbank_id(self):
#         # query=PaymentTransaction.objects.filter(bank_id="c18935cc-2a33-40a6-ad99-50b3a00e3d6d")
#         query=PaymentTransaction.objects.all()
#         serializer=CustomerPaymentTransactionSerializer(instance=query, many=True)
#         return serializer.data
#     class Meta:
#         model=PaymentTransaction
#         fields='__all__'
#         depth=1

# # GET COA By ID Seriallizer Customer Payment
# class COACustomerPaymentSerializer(serializers.ModelSerializer):
#     coa_cp=CustomerPaymentTransactionSerializer(many=True)    
#     class Meta:
#         model=COA
#         fields=['coa_cp']
 
#  # GET COA By ID Seriallizer Customer Payment
# class COACustomerPaymentSerializer(serializers.ModelSerializer):
#     # coa_cp=CustomerPaymentTransactionSerializer(many=True)
#     customer_payment=serializers.SerializerMethodField('getbank_id')
#     def getbank_id(self, customer):
#         query=PaymentMade.objects.filter(bank_id="c18935cc-2a33-40a6-ad99-50b3a00e3d6d", customer_id=customer)
#         serializer=CustomerPaymentTransactionSerializer(instance=query, many=True)
#         return serializer.data
#     class Meta:
#         model=COA
#         fields=['coa_cp']
################################################
#DFOA Serializer
# Deposit From Other Account Serializer
class DFOASerializer(serializers.ModelSerializer):
    class Meta:
        model=DFOA
        fields='__all__'

#Deposit Form Other Account Transaction
class DFOATransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=DFOATransaction
        fields='__all__'
        depth=1

# GET COA By ID Seriallizer DFOA
class COADFOASerializer(serializers.ModelSerializer):
    dfoa_coa=DFOATransactionSerializer(many=True)
    class Meta:
        model=COA
        fields=['dfoa_coa']       

#########################################
#vendor advanced serializer
class VendorAdvancedSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorAdvanced
        fields='__all__'
        depth=1

#vendor advanced transaction serializer
class VendorAdvancedTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorAdvancedTransaction
        fields= '__all__'
        depth=1
#nested serializer for vendor advanced serializer coa
class COASerializer(serializers.ModelSerializer):
    coa_advancedvendor=VendorAdvancedTransactionSerializer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ('coa_id', 'coa_advancedvendor')

###################################################
#OwnerDrawingSerializer
class OwnerDrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model=OwnerDrawing
        fields= '__all__'

# OwnerdrawingTransactionSerializer     
class OwnerdrawingTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=OwnerDrawingTransaction
        fields= '__all__'
        depth=1
      
# nested serializer for owner drawing
class COAForOwnerDrawingSerializer(serializers.ModelSerializer):
    coa_ownerwithdraw=OwnerdrawingTransactionSerializer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ('coa_id', 'coa_ownerwithdraw')

########################################
#CreditNote Serializer
#credit noterefund transaction  serializer

class CNRTSerializer(serializers.ModelSerializer):
    class Meta:
        model=CreditNoteRefundTransaction
        fields= '__all__'
        depth=1

# credit note refund transaction
class CreditNoteRefundSerialiser(serializers.ModelSerializer):
    class Meta:
        model=RefundMaster
        fields= '__all__'


#nested serializer for credit note transaction serializer
class CoaForCNRTSerializer(serializers.ModelSerializer):
    coa_creditnoterefund=CNRTSerializer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ('coa_id','coa_creditnoterefund')

# GET Customer id by 
class CNCustomerSerializer(serializers.ModelSerializer):
    customer_cn=CreditNoteRefundSerialiser(many=True)
    class Meta:
        model=SalesCustomer
        fields=['customer_cn']

#Get CN_Status In Credit Note
class CreditNoteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=CreditNote
        fields=['cn_status']

# Get Cn_Status in Customer id
class CNStatusCustomerSerializer(serializers.ModelSerializer):
    cnsta_customer=CreditNoteStatusSerializer(many=True)
    class Meta:
        model=SalesCustomer
        fields=['cnsta_customer']


class CreditNoteRefSerializer(serializers.ModelSerializer):
    class Meta:
        model=CreditNote
        fields="__all__"

class GETCreditNoteCustomerSerializer(serializers.ModelSerializer):
    customer_cn=serializers.SerializerMethodField('getopen_status')
    def getopen_status(self, customer):
        query=CreditNote.objects.filter(status='Open', customer_id=customer)
        serializer=CreditNoteRefSerializer(instance=query, many=True)
        return serializer.data
    class Meta:
        model=SalesCustomer
        fields=['customer_cn']
        depth=1

#####################################################
# Other Income Serializer
class OtherIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model=OtherIncome
        fields= '__all__'

#Other Income Transaction serializer

class OITSerializer(serializers.ModelSerializer):
    class Meta:
        model=OtherIncomeTransaction
        fields= '__all__'
        depth=1

# Nested Serializer Other Income

class COAOISerializer(serializers.ModelSerializer):
    coa_otherincome=OITSerializer (many=True,read_only=True)
    class Meta:
        model=COA
        fields= ('coa_id','coa_otherincome')
	  
########################################################
#ExpenseRefund Serializer
class ExpenseRefundSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExpenseRefund
        fields= '__all__'

# ExpnseRefund Transaction Serializer
class ExpRefundTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExpRefundTransaction
        fields= '__all__'
        depth=1

# Nested Serializer Expense Serializer
class COAExpenseRefundSerializer(serializers.ModelSerializer):
    coa_exp=ExpRefundTransactionSerializer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ('coa_id','coa_exp')
####################################################
#Interest Income Serializer
class InterestIncomeSerialiser(serializers.ModelSerializer):
    class Meta:
        model=InterestIncome
        fields= '__all__'

# Interest Income Transaction Serializer

class InterestIncomeTransactionSerlizer(serializers.ModelSerializer):
    class Meta:
        model=InterestIncomeTransaction
        fields= '__all__'
        depth=1

# Nested Serializer Interest Income

class COAforInterestIncomeSerializer(serializers.ModelSerializer):
    coa_interestincome=InterestIncomeTransactionSerlizer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ('coa_id','coa_interestincome')
	  

#################################################################


#OwnersContribution serializer

class OwnersContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model=OwnersContribution
        fields='__all__'

#OwnersContribution transaction serializer

class OwnersContributionTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=OwnersContributionTransaction
        fields= '__all__'
        depth=1
#OwnersContribution nested serializer

class COAOCSerializer(serializers.ModelSerializer):
    coa_ownerscontribution=OwnersContributionTransactionSerializer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ('coa_id', 'coa_ownerscontribution')
        
##########################################################
#Debit Note Refund
# DebitNoteRefund Serializer

class DebitNoteRefundSerializer(serializers.ModelSerializer):
    class Meta:
        model=RefundMaster
        fields= '__all__'

#DebitNoteRefundTransaction serializer

class DNRTSerializer(serializers.ModelSerializer):
    class Meta:
        model=DebitNoteRefundTransaction
        fields= '__all__'
        depth=1

# DebitNote Nested Serializer by COA

class COADebitNoteRefundSerializer(serializers.ModelSerializer):
    coa_debitnoteref=DNRTSerializer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ('coa_id', 'coa_debitnoteref')
		
#DebitNote Serializer In Status show 

class DebitNoteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=purchase.models.DebitNote
        fields= ['dn_status']



# DebitNote Status Get By Vendor Id
class VendordDNSerializer(serializers.ModelSerializer):
    ven_debitnote=DebitNoteStatusSerializer(many=True, read_only=True)
    class Meta:
        model=purchase.models.Vendor
        fields= ('vendor_id', 'ven_debitnote')

# DebitNote Get By Vendor Id
class DebitNoteVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=purchase.models.DebitNote
        fields= '__all__'

class VendorDebitNoteRefSerializer(serializers.ModelSerializer):
    ven_debitnote=serializers.SerializerMethodField('getopen_status')
    def getopen_status(self, vendor):
        query=purchase.models.DebitNote.objects.filter(status='Open', vendor_id=vendor)
        serializer=DebitNoteVendorSerializer(instance=query, many=True)
        return serializer.data
    class Meta:
        model=purchase.models.Vendor
        fields= ["ven_debitnote"]
        depth=1


#ExpenseBank serializer
class ExpbankSerializer(serializers.ModelSerializer):
    class Meta:
        model=purchase.models.ExpenseRecord
        fields='__all__'

#ExpenseBankTransaction serializer
class ExpbankjtSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExpenseBankTransaction
        fields= '__all__'
        depth=1


# ExpenseBank Nested Serializer
class COAExpBankSerializer(serializers.ModelSerializer):
    coa_expbank=ExpbankjtSerializer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ('coa_id', 'coa_expbank')
	  
#Transfer from another account  serializer

class TFAASerializer(serializers.ModelSerializer):
    class Meta:
        model=TransferFromAnotherAccount
        fields='__all__'

#Transfer From Another Account Transaction serializer

class TFAATransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=TransferFromAnotherAccountTransaction
        fields= '__all__'
        depth=1

#Nested serializer for Transfer from another account  serializer

class COAforTFAA(serializers.ModelSerializer):
    coa_tfaadata=TFAATransactionSerializer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ('coa_id', 'coa_tfaadata')
#Vendor PaymentRefund Serializer

class VendorPaymentRefSerializer(serializers.ModelSerializer):
    class Meta:
        model=RefundMaster
        fields= '__all__'
    
class VendorPaymentGETSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorAdvanced
        fields= "__all__"



class VendorpaymenttrefSerializer(serializers.ModelSerializer):
    vendor_py=serializers.SerializerMethodField('getamount')
    def getamount(self, vendor):
        query=VendorAdvanced.objects.filter(balance_amount__gt=0, vendor_id=vendor)
        serializer=VendorPaymentGETSerializer(instance=query, many=True)
        return serializer.data
    class Meta:
        model=purchase.models.Vendor
        fields= ['vendor_py']
        depth=1


#VendorPaymentRefund Transaction Serializer
class VendorPaymentRefTransSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorPaymentRefTransaction
        fields= '__all__'
        depth=1
#
##VendorPaymentRefund Nested Serializer
class VPRbyVidSerializer(serializers.ModelSerializer):
    vid_excessamount=VendorPaymentRefSerializer(many=True, read_only=True)
    class Meta:
        model=purchase.models.Vendor
        fields= ('vendor_id', 'vid_excessamount')

# VendorPaymentRefundTransaction Get By Coa id
class COAVendorPaymentRefundSerializer(serializers.ModelSerializer):
    coa_vendorpaymentref=VendorPaymentRefTransSerializer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ['coa_id', 'coa_vendorpaymentref']

#Payment Made Serialize

class VendorPaymentMadeSerializer(serializers.ModelSerializer):
    class Meta:
        model=purchase.models.PaymentMade
        fields= ['pm_id','payment_serial','amount_payable','balance_amount','amount_due','amount_excess']

# Get Excess Amount By Vendor Id
class VendorExAmountSerializer(serializers.ModelSerializer):
    coa_vp=VendorPaymentMadeSerializer(many=True, read_only=True)
    class Meta:
        model=purchase.models.Vendor
        fields=['vendor_id','coa_vp']

#####################################################################
#Vendor Payment Serializer
class VendorPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorPayment
        fields= '__all__'


#VendorPaymentRefund Transaction Serializer
class VendorPaymentTransSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorPaymentTransaction
        fields= '__all__'
        depth=1

#GET Coa id By Vendor Payment
class COAVendorPaymentSerializer(serializers.ModelSerializer):
    coa_vendorpayment=VendorPaymentTransSerializer(many=True, read_only=True)
    class Meta:
        model=COA
        fields= ['coa_id', 'coa_vendorpayment']

#payment journal transaction
# class PaymentJournalTransSerializer(serializers.ModelSerializer):          
#         #PaymentTransaction.objects.exclude(bank_id__exact='')

#         # for below code we are facing error for filter have to check once    
#         # pr_coa=serializers.SerializerMethodField('getbank_id')
#         # def getbank_id(self):
#         #     query=PaymentTransaction.objects.filter(bank_id__isnull=False)
#         #     serializer=PaymentJournalTransSerializer(instance=query, many=True)
#         #     return serializer.data   
#         class Meta:
#             model = PaymentTransaction
#             fields = '__all__'
#             depth=1

#GET Coa id By customer Payment
# class COACustomerPaymentSerializer(serializers.ModelSerializer):
#     pr_coa=PaymentJournalTransSerializer(many=True, read_only=True)
#     class Meta:
#         model=COA
#         fields= ['coa_id', 'pr_coa']
        #fields='__all__'
        
# #payment journal transaction
# class PaymentMadeJournalTransSerializer(serializers.ModelSerializer):         
#         class Meta:
#             model =purchase.models.PaymentmadeJournalTransaction
#             fields = '__all__'
#             depth=1

#GET Coa id By customer Payment
# class COACustomerPaymentSerializer(serializers.ModelSerializer):
#     pm_coa=PaymentJournalTransSerializer(many=True, read_only=True)
#     class Meta:
#         model=COA
#         fields= ['coa_id', 'pm_coa']

# All bank transactins 
class allbanktransactionserializer(serializers.ModelSerializer):
    ttaa_coa=TTAATransctionSerializer(many=True)
    cardpayment_coa=CardPaymentTransactionSerializer(many=True)
    coa_ownerwithdraw=OwnerdrawingTransactionSerializer(many=True)
    dtoa_coa=DTOATransactionSerializer(many=True)
    coa_tfaadata=TFAATransactionSerializer(many=True)
    coa_interestincome=InterestIncomeTransactionSerlizer(many=True)
    coa_otherincome=OITSerializer (many=True)
    coa_exp=ExpRefundTransactionSerializer(many=True)
    dfoa_coa=DFOATransactionSerializer(many=True)
    coa_ownerscontribution=OwnersContributionTransactionSerializer(many=True, read_only=True)
    coa_advancedvendor=VendorAdvancedTransactionSerializer(many=True, read_only=True)
    #coa_vendorpayment=VendorPaymentTransSerializer(many=True, read_only=True)
    coa_ca=CustomerAdvancedTransctionSerializer(many=True)
    #coa_cp=CustomerPaymentTransactionSerializer(many=True)
    coa_vendorpaymentref=VendorPaymentRefTransSerializer(many=True, read_only=True)
    coa_debitnoteref=DNRTSerializer(many=True, read_only=True)
    coa_expbank=ExpbankjtSerializer(many=True, read_only=True)
    coa_creditnoterefund=CNRTSerializer(many=True, read_only=True)
    coa_paymentref=PaymentRefundTransctionSerializer(many=True)
    # pr_coa=PaymentJournalTransSerializer(many=True)#, allow_null=False
    # pm_coa=PaymentMadeJournalTransSerializer(many=True, read_only=True)


    class Meta:
        model=Banking
        fields='__all__'
        depth=1




############################ SERIALIZER MADE BY VARSHA #############################3

class UpdateCustomerAdvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerAdvance
        fields='__all__'
        
        
class UpdateVendorAdvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorAdvanced
        fields='__all__'