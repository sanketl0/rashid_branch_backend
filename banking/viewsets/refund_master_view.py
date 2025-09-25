import json
import os
from pathlib import Path

import uuid
from rest_framework.response import Response
from rest_framework import viewsets
from company.models import Company,Branch,Company_Year
from coa.models import COA
from transaction.models import MasterTransaction
from banking.models.banking_model import Banking
from banking.models.refund_master_model import RefundMaster
from banking.serializers.refund_master_serializers import Refund_Serializer
from salescustomer.models import SalesCustomer
from banking.models.customer_advance_model import CustomerAdvance
from salescustomer.models.Creditnote_model import CreditNote
from purchase.models.Vendor_model import Vendor
from purchase.models.Debitnote_model import DebitNote
from banking.models.vendor_advanced_model import VendorAdvanced
from audit.models import Audit
#Payment Refund
from django.db import transaction
class PaymentRefundViewsets(viewsets.ModelViewSet):
    queryset =RefundMaster.objects.all()
    serializer_class =Refund_Serializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction

    def ValidateDefaults(obj):
        PaymentRefundViewsets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
       
        retValue=True
        if branch_id is None:
            PaymentRefundViewsets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            PaymentRefundViewsets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            PaymentRefundViewsets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False
             
        return retValue
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        paymentrefund_data= request.data

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=paymentrefund_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)
        user = request.user

        if(PaymentRefundViewsets.ValidateDefaults(paymentrefund_data)==False):
            print(" Ooops!!! Error Occured ",PaymentRefundViewsets.logger)
        
        print(paymentrefund_data)

       # Branch and Company Null value

        branch_id=paymentrefund_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=paymentrefund_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        customer_id=paymentrefund_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)
            
        # company_year_id=paymentrefund_data.get("company_year_id")
        # if company_year_id is not None:
        #     company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

        Customeradvanced_id=paymentrefund_data["ca_id"]
        print("Customer Advanced id is ",Customeradvanced_id,type(Customeradvanced_id))

        is_bank_transaction="True"
        if is_bank_transaction == "True":
            
            
            #Creat Payment Refund
            paymentrefund_id=RefundMaster.objects.create(
            company_id=company_id,
            customer_id=customer_id,
            branch_id=branch_id,
            bank_id=From_Bank,
            is_bank_transaction=True,
            refrence_id=Customeradvanced_id,
            coa_id=COA.objects.get(coa_id=paymentrefund_data["coa_id"]),
            refund_date=paymentrefund_data["payment_refund_date"],
            is_cust_advance_refund_generated=paymentrefund_data["is_payment_refund_generated"],
            refund_ref_no=paymentrefund_data["payment_refund_ref_no"],
            payment_mode=paymentrefund_data["paid_via"],
        # form_type=paymentrefund_data["form_type"],
            status=paymentrefund_data  ["status"],
            serial_ref=paymentrefund_data["payment_serial"],
            description=paymentrefund_data["description"],
            balance_amount_ref=paymentrefund_data["amount_excess"],
            amount_ref=paymentrefund_data["amount_received"])
            paymentrefund_id.save()
            print(paymentrefund_id)

            Audit.objects.create(
                company_id=company_id,
                branch_id=branch_id,
                created_by=user,
                audit_created_date=paymentrefund_data["payment_refund_date"],
                module="Banking",
                sub_module='Customer Advanced Refund',
                data=paymentrefund_data
            )
            custadv=CustomerAdvance.objects.get(ca_id=paymentrefund_data['ca_id'])
            TO_COA= COA.objects.get(company_id=company_id,account_subhead="Account Receivables",isdefault=True)
            print('""""""""""""',TO_COA)  
            paymnetmast=MasterTransaction.objects.create(
            L1detail_id=paymentrefund_id.rm_id,
            L1detailstbl_name='Refund Master',
            L2detail_id=From_Bank.bank_id,
            L2detailstbl_name='BANK',
            L3detail_id=custadv.ca_id,
            L3detailstbl_name='Customer Advanced',
            main_module='Banking',
            module='MonenyOut',
            sub_module='Customer Advanced Refund',
            transc_deatils='Customer Advanced refund',
            banking_module_type=paymentrefund_data["transaction_module"],
            journal_module_type=paymentrefund_data["transaction_module"],
            trans_date=paymentrefund_data["payment_refund_date"],
            trans_status=paymentrefund_data["status"],
            debit=paymentrefund_data["amount"],
            to_account=TO_COA.coa_id,
            to_acc_type=TO_COA.account_type,
            to_acc_head=TO_COA.account_head,
            to_acc_subhead=TO_COA.account_subhead,
            to_acc_name=TO_COA.account_name,
            credit=paymentrefund_data['amount'],
            from_account=From_Bank.coa_id.coa_id,        
            from_acc_type=From_Bank.coa_id.account_type,
            from_acc_head=From_Bank.coa_id.account_head,
            from_acc_subhead=From_Bank.coa_id.account_subhead,
            from_acc_name=From_Bank.coa_id.account_name,
            company_id=company_id,
            customer_id=customer_id,
            branch_id=branch_id)
            paymnetmast.save() 
            
    

            ca_id=paymentrefund_data["ca_id"]
            if ca_id is not None:
                ca_id=CustomerAdvance.objects.get(ca_id=ca_id)

                balance_amount=float(paymentrefund_data["amount_excess"])
                
                print("Amount values are",balance_amount,type(balance_amount))
                if balance_amount > 0:
                    print('Customer Advanced id of else', ca_id)
                    ca_id.balance_amount= paymentrefund_data["amount_excess"]            
                    ca_id.save()       
                    print('Customer Advanced amount updated to ', ca_id.balance_amount)
                else:     
                    print('ca_id', ca_id)              
                    print('Customer Advanced status is Not updated ')
                
            else:
                print("Balance Amount is Low")

            serializer = Refund_Serializer(paymentrefund_id)
            return Response(serializer.data)








from django.db import transaction



class DebitNoteRefundModelViewSets(viewsets.ModelViewSet):
    queryset=RefundMaster.objects.all()
    serializer_class=Refund_Serializer


    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        DebitNoteRefundModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        vendor_id=obj["vendor_id"]
        retValue=True
        if vendor_id is None:
            DebitNoteRefundModelViewSets.logger.append("Vendor  iD is Null Please Provide a Vendor ID")
            retValue= False  
        if branch_id is None:
            DebitNoteRefundModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            DebitNoteRefundModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            DebitNoteRefundModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        debitnote_data = request.data

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=debitnote_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)

        if(DebitNoteRefundModelViewSets.ValidateDefaults(debitnote_data) == False):
            print(" Ooops!!! Error Occured ",DebitNoteRefundModelViewSets.logger)
            
        print(debitnote_data)
            #What if this ID is null , 
        	
        branch_id=debitnote_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=debitnote_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        vendor_id=debitnote_data["vendor_id"]
        if vendor_id is not None:
            vendor_id=Vendor.objects.get(vendor_id=vendor_id)
            
        # company_year_id=debitnote_data..get("company_year_id")
        # if company_year_id is not None:
        #     company_year_id=Company_Year.objects.get(company_year_id=company_year_id)


        debitnote_id=debitnote_data["dn_id"]
        print("debit note id is ",debitnote_id,type(debitnote_id))

        is_bank_transaction="True"
        if is_bank_transaction == "True":
            
        # Create DebitNoteRefund

            debit_id=RefundMaster.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            bank_id=From_Bank,
            vendor_id=vendor_id,
            refrence_id=debitnote_id,
            is_bank_transaction=True,
            coa_id=COA.objects.get(coa_id=debitnote_data["coa_id"]),
            is_dn_refund_generated=debitnote_data["is_dn_refund_generated"],
            refund_date=debitnote_data["refund_on"],
            status=debitnote_data["status"],
            refund_balance_amount=debitnote_data["refund_balance_amount"],
            refund_ref_no=debitnote_data["refund_ref_no"],
            amount=debitnote_data["amount"],
            payment_mode=debitnote_data["payment_mode"],
            serial_ref=debitnote_data["dn_serial"],
            amount_ref=debitnote_data["dn_amount"],
            description=debitnote_data["description"])
            debit_id.save()
            print("Debit Note Refund",debit_id,type(debit_id))




            
            

    #region  Master Transaction Section

            TO_COA = COA.objects.get(company_id=company_id,account_name="Account Payables",isdefault=True)
            print('""""""""""""',TO_COA)  
            dnrmast=MasterTransaction.objects.create(
            L1detail_id=debit_id.rm_id,
            L1detailstbl_name='RefundMaster',
            L2detail_id=From_Bank.bank_id,
            L2detailstbl_name='BANK',
            L3detail_id=debitnote_id,
            L3detailstbl_name='Debit Note',
            main_module='Banking',
            module='MonenyIN',
            sub_module='DebitNote Refund',
            transc_deatils='Debit Note Refund',
            banking_module_type=debitnote_data["transaction_module"],
            journal_module_type=debitnote_data["transaction_module"],
            trans_date=debitnote_data["refund_on"],
            trans_status=debitnote_data["status"],
            debit=debitnote_data["amount"],
            to_account=From_Bank.coa_id.coa_id,
            to_acc_type=From_Bank.coa_id.account_type,
            to_acc_head=From_Bank.coa_id.account_head,
            to_acc_subhead=From_Bank.coa_id.account_subhead,
            to_acc_name=From_Bank.coa_id.account_name,
            credit=debitnote_data['amount'],
            from_account=TO_COA.coa_id,
            from_acc_type=TO_COA.account_type,
            from_acc_head=TO_COA.account_head,
            from_acc_subhead=TO_COA.account_subhead,
            from_acc_name=TO_COA.account_name,
            company_id=company_id,
            vendor_id=vendor_id,
            branch_id=branch_id)
            dnrmast.save() 
            
    #endregion 
    #End MasterTransaction Section
            dn_id=debitnote_data["dn_id"]
            if dn_id is not None:
                dn_id=DebitNote.objects.get(dn_id=dn_id)

                balance_amount=float(debitnote_data["refund_balance_amount"])
                print("Amount values are",balance_amount,type(balance_amount))
                if balance_amount == 0:
                    print('dn_id', dn_id)
                    dn_id.balance_amount= debitnote_data["refund_balance_amount"]           
                    dn_id.dn_status='Closed'
                    dn_id.save()
                    print('Debit status updated to ', dn_id.status)
            
                elif balance_amount >= 0:
                    print('debit note id of else', dn_id)
                    dn_id.balance_amount= debitnote_data["refund_balance_amount"]            
                    dn_id.save()       
                    print('Debit note amount due updated to ', dn_id.balance_amount)
                else:
                    print('dn_id', dn_id)              
                    dn_id.dn_status='open'
                    dn_id.save()
                    print('Debit note status updated to ', dn_id.status)
            serializer =Refund_Serializer(debit_id)         
            return Response(serializer.data)






from django.db import transaction

#CreditNoteRefund
	  
# CNRefund view
class CNRefundModelViewSets(viewsets.ModelViewSet):
    queryset=RefundMaster.objects.all()
    serializer_class=Refund_Serializer

    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        CNRefundModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        customer_id=obj["customer_id"]
        cn_id=obj["cn_id"]
        retValue=True
        if customer_id is None:
            CNRefundModelViewSets.logger.append("Customer iD is Null Please Provide a Customer ID")
            retValue= False        
        if branch_id is None:
            CNRefundModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            CNRefundModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            CNRefundModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False
        if(type(cn_id!=uuid)):
            CNRefundModelViewSets.logger.append("creditnote ID is not a Valid UUID Please Provide a valid creditnote ID ")
            retValue= False 

        return retValue
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        Cnrefund_data = request.data

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=Cnrefund_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)


        if(CNRefundModelViewSets.ValidateDefaults(Cnrefund_data)==False):
            print(" Ooops!!! Error Occured ",CNRefundModelViewSets.logger)
            
        print(Cnrefund_data)
            #What if this ID is null , 

        branch_id=Cnrefund_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=Cnrefund_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
        
        customer_id=Cnrefund_data["customer_id"]
        if customer_id is not None:
            customer_id=SalesCustomer.objects.get(customer_id=customer_id)
            
        company_year_id=Cnrefund_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

        creditnote_id=Cnrefund_data["cn_id"]
        print("cnid",creditnote_id,type(creditnote_id))
        is_bank_transaction="True"
        print("Bank Transaction", is_bank_transaction)
        if is_bank_transaction=="True": 

            cnrefund_id=RefundMaster.objects.create(
                company_id=company_id,
                branch_id=branch_id,
                bank_id=From_Bank,
                customer_id=customer_id,
                refrence_id=creditnote_id,
                coa_id=COA.objects.get(coa_id=Cnrefund_data["coa_id"]),
                refund_date=Cnrefund_data["refund_on"],
                is_cn_refund_generated=Cnrefund_data["is_cn_refund_generated"],
                status=Cnrefund_data["status"],
                is_bank_transaction=True,
                refund_ref_no=Cnrefund_data["refund_ref_no"],
                refund_balance_amount=Cnrefund_data["refund_balance_amount"],
                amount=Cnrefund_data["amount"],
                serial_ref=Cnrefund_data["cn_serial"],
                amount_ref=Cnrefund_data["cn_amount"],
                payment_mode=Cnrefund_data["payment_mode"],
                description=Cnrefund_data["description"])
            cnrefund_id.save()
            print("Cnrefund_created",cnrefund_id,type(cnrefund_id))



         
#region Master Transaction Section

        TO_COA =COA.objects.get(company_id=company_id,account_subhead="Account Receivables",isdefault=True)
        print('""""""""""""',TO_COA)  
        CNRmast=MasterTransaction.objects.create(
        L1detail_id=cnrefund_id.rm_id,
        L1detailstbl_name='RefundMaster',
        L2detail_id=From_Bank.bank_id,
        L2detailstbl_name='BANK',
        L3detail_id=creditnote_id,
        L3detailstbl_name='Credit Note',
        main_module='Banking',
        module='MonenyOut',
        sub_module='CreditNoteRefund',
        transc_deatils='Credit Note Refund',
        banking_module_type=Cnrefund_data["transaction_module"],
        journal_module_type='Refund',
        trans_date=Cnrefund_data["refund_on"],
        trans_status=Cnrefund_data["status"],
        debit=Cnrefund_data["amount"],
        to_account=TO_COA.coa_id,
        to_acc_type=TO_COA.account_type,
        to_acc_head=TO_COA.account_head,
        to_acc_subhead=TO_COA.account_subhead,
        to_acc_name=TO_COA.account_name,
        credit=Cnrefund_data['amount'],
        from_account=From_Bank.coa_id.coa_id,        
        from_acc_type=From_Bank.coa_id.account_type,
        from_acc_head=From_Bank.coa_id.account_head,
        from_acc_subhead=From_Bank.coa_id.account_subhead,
        from_acc_name=From_Bank.coa_id.account_name,
        company_id=company_id,
        customer_id=customer_id,
        branch_id=branch_id)
        CNRmast.save() 

#endregion

#End Master Transaction Section Credit Note refund

        cn_id=Cnrefund_data["cn_id"]
        if cn_id is not None:
            cn_id=CreditNote.objects.get(cn_id=cn_id)

            balance_amount=float(Cnrefund_data["refund_balance_amount"])
            print("Amount values are",balance_amount,type(balance_amount))
            if balance_amount == 0:
            # cn_id =cn_id      
                print('cn_id', cn_id)              
                cn_id.status='Closed'
                cn_id.save()
                print('creditnote status updated to ', cn_id.status)
           
            elif balance_amount >= 0:
            # cn_id = cn_id
                print('credit note id of else', cn_id)
                cn_id.balance_amount= Cnrefund_data["refund_balance_amount"]            
                cn_id.save()       
                print('credinote amount due updated to ', cn_id.balance_amount)
            else:
            # cn_id =cn_id      
                print('cn_id', cn_id)              
                cn_id.status='open'
                cn_id.save()
                print('creditnote status updated to ', cn_id.status)
        
        
        serializer =Refund_Serializer(cnrefund_id)
        return Response(serializer.data)


from django.db import transaction

###########################################################################
#Vendor Advance Refund
# VendorPaymentRefund View Sets
class VendorPaymentRefModelViewSets(viewsets.ModelViewSet):
    queryset=RefundMaster.objects.all()
    serializer_class=Refund_Serializer

    
    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        VendorPaymentRefModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        vendor_id=obj["vendor_id"]
        retValue=True
        if vendor_id is None:
            VendorPaymentRefModelViewSets.logger.append("Vendor iD is Null Please Provide a Vendor ID")
            retValue= False     
        if branch_id is None:
            VendorPaymentRefModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            VendorPaymentRefModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            VendorPaymentRefModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue    
    

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        vpr_data = request.data

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        bank=vpr_data["coa_id"]
        From_Bank=Banking.objects.get(coa_id=bank)

        if(VendorPaymentRefModelViewSets.ValidateDefaults(vpr_data)==False):
            print(" Ooops!!! Error Occured ",VendorPaymentRefModelViewSets.logger)
            
        print(vpr_data)
            #What if this ID is null , 
        	
        branch_id=vpr_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=vpr_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)       


        vendor_id=vpr_data["vendor_id"]
        if vendor_id is not None:
            vendor_id=Vendor.objects.get(vendor_id=vendor_id)

        Vendoradvanced_id=vpr_data["va_id"]
        print("vendor Advanced id is ",Vendoradvanced_id,type(Vendoradvanced_id))
        
        is_bank_transaction="True"
        if is_bank_transaction == "True":
            

        # Create Vendor Payment Refund

            vpred_id=RefundMaster.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            bank_id=From_Bank,
            vendor_id=vendor_id,
            is_bank_transaction=True,
            refrence_id=vpr_data["va_id"],
            status=vpr_data["status"],
            coa_id=COA.objects.get(coa_id=vpr_data["coa_id"]),
            is_vend_advance_refund_generated=vpr_data["is_vendor_payment_refund_generated"],
            refund_date=vpr_data["vendor_payment_date"],
            serial_ref_no=vpr_data["vendor_payment_ref_no"],
            refund_balance_amount=vpr_data["amount_excess"],
            payment_mode=vpr_data["received_via"],
            amount=vpr_data["amount"],
            serial_ref=vpr_data["payment_serial"],
            description=vpr_data["description"])
            vpred_id.save()

    #region Master Transaction Section

            TO_COA =COA.objects.get(company_id=company_id,account_subhead='Account Payables',isdefault=True)
            vpcredittrans=MasterTransaction.objects.create(
            L1detail_id=vpred_id.rm_id,
            L1detailstbl_name='RefundMaster',
            L2detail_id=From_Bank.bank_id,
            L2detailstbl_name='BANK',
            L3detail_id=Vendoradvanced_id,
            L3detailstbl_name='Vendor Advanced',
            main_module='Banking',
            module='MonenyIN',
            sub_module='Vendor Advanced Payment',
            transc_deatils='Vendor Advanced Payment',
            banking_module_type=vpr_data["transaction_module"],
            journal_module_type=vpr_data["transaction_module"],
            trans_date=vpr_data["vendor_payment_date"],
            trans_status=vpr_data["status"],
            debit=vpr_data["amount"],
            to_account=From_Bank.coa_id.coa_id,
            to_acc_type=From_Bank.coa_id.account_type,
            to_acc_head=From_Bank.coa_id.account_head,
            to_acc_subhead=From_Bank.coa_id.account_subhead,
            to_acc_name=From_Bank.coa_id.account_name,
            credit=vpr_data['amount'],
            from_account=TO_COA.coa_id,
            from_acc_type=TO_COA.account_type,
            from_acc_head=TO_COA.account_head,
            from_acc_subhead=TO_COA.account_subhead,
            from_acc_name=TO_COA.account_name,
            company_id=company_id,
            vendor_id=vendor_id,
            branch_id=branch_id)
            vpcredittrans.save()      
        
    #endregion 
    #End Master Transaction Section

            va_id=vpr_data["va_id"]
            if va_id is not None:
                va_id=VendorAdvanced.objects.get(va_id=va_id)

                balance_amount=float(vpr_data["amount_excess"])
                
                print("Amount values are",balance_amount,type(balance_amount))
                if balance_amount >= 0:
                    print('Vendor Advanced id of else', va_id)
                    va_id.balance_amount= vpr_data["amount_excess"]            
                    va_id.save()       
                    print('Vendor Advanced Amount updated to ', va_id.balance_amount)
                else:     
                    print('cn_id', va_id)              
                    print('Vendor Advanced status is Not updated ')
                

            serializer =Refund_Serializer(vpred_id)         
            return Response(serializer.data)	   



class NewVendor_debitRefundModelViewSets(viewsets.ModelViewSet):
    queryset=RefundMaster.objects.all()
    serializer_class=Refund_Serializer


    logger=[]
    # Forone API are going to make three append append namely for Two Main Sections
      #  1: Table Details:Details of the Table which stores the Descriotion and the metadata
      #  2: Financial Transaction: 
        #2.1 Credit Transation
        #2.2 Debit Transaaction
    def ValidateDefaults(obj):
        NewVendor_debitRefundModelViewSets.logger=[]
        ## Validation Section
        branch_id=obj["branch_id"]
        company_id=obj["company_id"]
        vendor_id=obj["vendor_id"]
        retValue=True
        if vendor_id is None:
            NewVendor_debitRefundModelViewSets.logger.append("Vendor  iD is Null Please Provide a Vendor ID")
            retValue= False  
        if branch_id is None:
            NewVendor_debitRefundModelViewSets.logger.append("Branch iD is Null Please Provide a Branch ID")
            retValue= False        
        if(company_id is  None ):
            NewVendor_debitRefundModelViewSets.logger.append("company ID is Null Please Provide a company ID")
            retValue= False            
        if(type(company_id!=uuid)):
            NewVendor_debitRefundModelViewSets.logger.append("company ID is not a Valid UUID Please Provide a valid company ID ")
            retValue= False      
        return retValue

    def create(self, request, *args, **kwargs):
        debitnote_data = request.data
        

        # GET coa_id in Banking and Pass the bank_id Transaction Table and Main Details Table
        # bank=debitnote_data["coa_id"]
        # From_Bank=Banking.objects.get(coa_id=bank)

        if(NewVendor_debitRefundModelViewSets.ValidateDefaults(debitnote_data)==False):
            print(" Ooops!!! Error Occured ",NewVendor_debitRefundModelViewSets.logger)
            
        print(debitnote_data)
            #What if this ID is null , 
        	
        branch_id=debitnote_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_id=debitnote_data["company_id"]
        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)

        vendor_id=debitnote_data["vendor_id"]
        if vendor_id is not None:
            vendor_id=Vendor.objects.get(vendor_id=vendor_id)


        debitnote_id=debitnote_data["dn_id"]
        print("debit note id is ",debitnote_id,type(debitnote_id))

        # Create DebitNoteRefund

        debit_id=RefundMaster.objects.create(
        company_id=company_id,
        branch_id=branch_id,
        bank_id=debitnote_data["bank_id"],
        vendor_id=vendor_id,
        refrence_id=debitnote_id,
        coa_id=COA.objects.get(coa_id=debitnote_data["coa_id"]),
        is_dn_refund_generated=debitnote_data["is_dn_refund_generated"],
        refund_date=debitnote_data["refunded_on"],
        status=debitnote_data["status"],
        refund_balance_amount=debitnote_data["refund_balance_amount"],
        refund_ref_no=debitnote_data["refund_ref_no"],
        amount=debitnote_data["amount"],
        payment_mode=debitnote_data["payment_mode"],
        serial_ref=debitnote_data["dn_serial"],
        amount_ref=debitnote_data["dn_amount"],
        description=debitnote_data["description"])
        debit_id.save()
        print("Debit Note Refund",debit_id,type(debit_id))




        
        #2 Financial Transaction Prerequisites 
        ## Credit Transaction 
        ## SHould be added the amount TO_COA_ID 
        # Refer the Excel coa_id refers  Bank COA it depends on the Form whether it is To_COA or From_COA

      
         # Get The COA Table  Account Name is Account Payables and Pass The coa_id in Debit Note Refund Transaction Table 

        
#Commenting By Shubham
# This Region is the Credit And Debit Transaction the vlaues are Two rows Added in Database


       
        TO_COA = COA.objects.COA.get_account_paybles(company_id)
        From_COA=COA.objects.get(company_id=company_id,coa_id=debitnote_data["coa_id"])
        print('""""""""""""',TO_COA)  
        dnrmast=MasterTransaction.objects.create(
        L1detail_id=debit_id.rm_id,
        L1detailstbl_name='RefundMaster',
        L2detail_id=From_COA.coa_id,
        L2detailstbl_name='COA',
        L3detail_id=debitnote_id,
        L3detailstbl_name='Debit Note',
        main_module='Banking',
        module='MonenyIN',
        sub_module='DebitNote Refund',
        transc_deatils='Debit Note Refund',
        banking_module_type=debitnote_data["transaction_module"],
        journal_module_type=debitnote_data["transaction_module"],
        trans_date=debitnote_data["refunded_on"],
        trans_status=debitnote_data["status"],
        debit=debitnote_data["amount"],
        to_account=From_COA.coa_id,
        to_acc_type=From_COA.account_type,
        to_acc_head=From_COA.account_head,
        to_acc_subhead=From_COA.account_subhead,
        to_acc_name=From_COA.account_name,
        credit=debitnote_data['entered_amount'],
        from_account=TO_COA.coa_id,
        from_acc_type=TO_COA.account_type,
        from_acc_head=TO_COA.account_head,
        from_acc_subhead=TO_COA.account_subhead,
        from_acc_name=TO_COA.account_name,
        company_id=company_id,
        vendor_id=vendor_id,
        branch_id=branch_id)
        dnrmast.save() 

#Balance Amount Update section
# refund time Update the status and dn_status or balance_amount
        dn_id=debitnote_data["dn_id"]
        if dn_id is not None:
            dn_id=DebitNote.objects.get(dn_id=dn_id)

            balance_amount=debitnote_data["refund_balance_amount"]
            print("Amount values are",balance_amount,type(balance_amount))
            if balance_amount == 0:
                print('dn_id', dn_id)
                dn_id.balance_amount= debitnote_data["refund_balance_amount"]           
                dn_id.status='Closed'
                dn_id.dn_status='Closed'
                dn_id.save()
                print('Debit status updated to ', dn_id.status)
           
            elif balance_amount >= 0:
                print('debit note id of else', dn_id)
                dn_id.balance_amount= debitnote_data["refund_balance_amount"]            
                dn_id.save()       
                print('Debit note amount due updated to ', dn_id.balance_amount)
            else:
                print('dn_id', dn_id)              
                dn_id.status='open'
                dn_id.save()
                print('Debit note status updated to ', dn_id.status)
        serializer =Refund_Serializer(debit_id)         
        return Response(serializer.data)

#End Debit Note refund Section  

