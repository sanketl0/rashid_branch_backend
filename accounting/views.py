from ast import Not
from django.shortcuts import render
from html5lib import serialize
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from company.models import Company_Year

from purchase.models import Vendor
from .models import Company, Branch, JournalTransaction
from coa.models import COA
from salescustomer.models.Salescustomer_model import SalesCustomer

from .serializers import *

from transaction .models import MasterTransaction
from item.models.stock_model import Stock
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.db import transaction
from audit.models import Audit
#POST journal_transactions. this entry should go to the two table first is manual journal and second is journal transaction table
class journalViewSet(viewsets.ModelViewSet):
    queryset = JournalTransaction.objects.all()
    serializer_class = JournalTransactionSerializer


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        journal_data = request.data
        print("journal_data", journal_data)

        branch_id=journal_data["branch_id"]
        if branch_id is not None:
            branch_id=Branch.objects.get(branch_id=branch_id)

        company_year_id=journal_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

        journal_transactions=journal_data["journal_transactions"]
        comp_id = Company.objects.get(company_id=journal_data["company_id"])
        #branch_id = Branch.objects.get(branch_id=journal_data["branch_id"])

        #manual journals fields        
        journal_id=ManualJournal.objects.create(journal_ref_no=journal_data["journal_ref_no"],
        journal_date=journal_data["journal_date"],
        journal_status=journal_data["journal_status"],
        journal_serial_no=journal_data["journal_serial_no"],        
        notes=journal_data["notes"],
        journal_type=journal_data["journal_type"],
        is_journal_generated=journal_data["is_journal_generated"],
        sub_total=journal_data["sub_total"],
        total=journal_data["total"],
        journal_amount=journal_data["journal_amount"],         
        company_id = comp_id,        
        branch_id = branch_id)
        journal_id.save()
        print("journal_transactions",journal_transactions,type(journal_transactions))        
        

        for i in range(len(journal_transactions)):            
                      
            new_journal = JournalTransaction.objects.create(mj_id=journal_id,
                       
            coa_id = COA.objects.get(coa_id=journal_transactions[i]["coa_id"]),
            company_id = comp_id,
            des=journal_transactions[i]["des"],
            date=journal_data["journal_date"],
            credit=journal_transactions[i]["credit"],
            debit=journal_transactions[i]["debit"])            
            new_journal.save()
            print(i,"journal_transactions")

        serializer = JournalTransactionSerializer(new_journal)         
        return Response(serializer.data)
    
    
    
#Manual Journal Trasaction  Creating section
    
class new1journalViewSet(viewsets.ModelViewSet):
    queryset = JournalTransaction.objects.all()
    serializer_class = JournalTransactionSerializer

    def create(self, request, *args, **kwargs):
        journal_data = request.data
        user = request.user
        return self.handle_post(user,journal_data)
    @transaction.atomic
    def handle_post(self,user, journal_data):
        # count = Feature.objects.get(user_id=request.user.id).journal_remaining
        # print(count, 'journal ')
        # if count <= 0:
        #     return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)
        journal_transactions = journal_data["journal_transactions"]
        total_credit = round(sum(float(transaction['credit']) for transaction in journal_transactions),2)
        total_debit = round(sum(float(transaction['debit']) for transaction in journal_transactions),2)
        print(total_debit,total_credit)
        if total_credit != total_debit:
            return Response({"message":"Journal total not matching"},status=400)

        print(journal_data)
        #check the null fields
        branch_id=journal_data["branch_id"]
        branch_id=Branch.objects.get(branch_id=branch_id)
            
        company_id=journal_data["company_id"]

        if company_id is not None:
            company_id=Company.objects.get(company_id=company_id)
            
        company_year_id=journal_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)

        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            created_by=user,
            audit_created_date=journal_data['journal_date'],
            module="Journal",
            sub_module="Journal",
            data=journal_data
        )

        
        #create journal 
        journal_id=ManualJournal.objects.create(journal_ref_no=journal_data["journal_ref_no"],
        journal_date=journal_data["journal_date"],
        journal_status=journal_data["journal_status"],
        journal_serial_no=journal_data["journal_serial_no"],        
        notes=journal_data["notes"],
        journal_type=journal_data["journal_type"],
        is_journal_generated=journal_data["is_journal_generated"],
        sub_total=journal_data["sub_total"],
        total=journal_data["total"],
        difference=journal_data["difference"],
        journal_amount=journal_data["journal_amount"],
        ext_id=journal_data.get("ext_id",None),
        ext_type=journal_data.get("ext_type",'TALLY'),
        company_id = company_id,
        branch_id = branch_id)
        journal_id.save()

        print("journal_transactions",journal_transactions,type(journal_transactions))

        #Selected contact Account
        for journal_transaction in journal_transactions:
            if journal_transaction['contact'] is not None:
                contact = journal_transaction['contact']
                customer = SalesCustomer.objects.filter(customer_id=contact)
                if customer.exists():
                    customer = customer[0]
                else:
                    customer = None
                vendor = None
                if customer is None:
                    vendor = Vendor.objects.filter(vendor_id=contact)
                    if vendor.exists():
                        vendor = vendor[0]
                    else:
                        vendor = None
            else:
                customer=None
                vendor=None
                #print('"""""',journal_transaction['selected_contact']['customer_id'])
           #Geting Coa    
            FROM_COA = COA.objects.get(coa_id=journal_transaction["coa_id"])
            TO_COA= COA.objects.get(coa_id=journal_transaction["coa_id"])
            dnmast = MasterTransaction.objects.create(
                L1detail_id=journal_id.mj_id,
                L1detailstbl_name='ManualJournal',
                main_module='Accounting',
                module='Accounting',
                sub_module='ManualJournal',
                transc_deatils='Manual Journal Transaction',
                banking_module_type='ManualJournal',
                journal_module_type='ManualJournal',
                trans_date=journal_data["journal_date"],
                trans_status='Manually Added',
                debit=journal_transaction["debit"],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=journal_transaction["credit"],
                from_account=FROM_COA.coa_id,
                from_acc_type=FROM_COA.account_type,
                from_acc_head=FROM_COA.account_head,
                from_acc_subhead=FROM_COA.account_subhead,
                from_acc_name=FROM_COA.account_name,
                company_id=company_id,
                branch_id=branch_id,
                customer_id=customer,
                vendor_id=vendor)
            dnmast.save()
            items = journal_transaction.get('items',[])
            for item in items:
                if item['debit'] > 0:
                    amt = float(item['debit'])
                    flow_type = 'INWARD'
                    stock_in = float(item['quantity'])
                    stock_out = 0
                else:
                    amt = float(item['credit'])
                    flow_type = 'OUTWARD'
                    stock_out = float(item['quantity'])
                    stock_in = 0
                mj_obj, created = Stock.objects.get_or_create(
                    item_id=item['item_id'],
                    item_name=item["item_name"],
                    ref_id=journal_id.mj_id,
                    flow_type=flow_type,
                    stock_in=stock_in,
                    stock_out=stock_out,
                    ref_tblname=journal_transaction["coa_id"],
                    formname='ManualJournal',
                    module_date=journal_id.created_date,
                    date = journal_data["journal_date"],
                    batch_no=item['batch_no'],
                    mfg_date=item['mfg_date'],
                    expire_date=item['expire_date'],
                    godown_id_id=item['godown_id'],
                    godown_name=item['godown_name'],
                    quantity=round(float(item['quantity']), 2),
                    amount=amt,
                    branch_id=branch_id,
                    company_id=company_id,
                    stage='Add Stages',
                    module="ManualJournal"
                )
          
        serializer = JournalTransactionSerializer(journal_id)         
        return Response(serializer.data,status=200)



#API POST for JournalTransaction
class journaltransactionViewSet(viewsets.ModelViewSet):
    queryset = JournalTransaction.objects.all()
    serializer_class = JournalTransactionSerializer



class journaltransactionList(generics.ListAPIView):
    queryset = JournalTransaction.objects.all()
    serializer_class = JournalTransactionSerializer




    
#Journal transaction and Manual journal join
class JournalTransactionGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = ManualJournal.objects.all()
    serializer_class = JoinJournalTransSerializer

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data' : self.retrieve(request, pk).data
            })
        return self.list(request)


#get the trasnsaction by manaual journal id
n_data=None
m_data=None
@api_view(['GET'])


def getmastermanualjournalshortbymjid(request,pk):
    master=MasterTransaction.objects.filter(L1detail_id=pk)
    manualjournal = ManualJournal.objects.filter(mj_id=pk)
    serializer=shortmanualjournalSerializer(manualjournal,many=True)
    print(serializer)
    serializem=MasterJournalSerializer(master,many=True)
    n_data=serializer.data
    m_data=serializem.data
    return Response({'data':n_data,'transaction':m_data})

#getshortDetails
@api_view(['GET'])
@renderer_classes([JSONRenderer])


def getmanualjournalshortbycompanyid(request,comp_id,branch_id):
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    objs = ManualJournal.objects.filter(company_id=comp_id,branch_id=branch_id)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": objs.count()
    }
    
    # Get the company object by comp_id and apply pagination
    try:

        manualjournal = objs.order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)
    response['results'] = JoinJournalTransSerializer(manualjournal, many=True).data
    return Response(response)


#getshortDetails
@api_view(['GET'])


def shortmanualjournalDetails(request):
    manualjournal = ManualJournal.objects.all()   
    serializer = shortmanualjournalSerializer(manualjournal, many=True)
    return Response(serializer.data)



#Get the all details in manual journal id wise
@api_view(['GET'])


def manualjournalDetail(request, pk):
    manualjournal = ManualJournal.objects.get(mj_id=pk)
    serializer = manualjournalSerializer(manualjournal, many=False)
    return Response(serializer.data)
#Put Method it ise to manual journala updated code wise
@api_view(['PUT'])


def manualjournalupdate(request, pk):
    manualjournal = ManualJournal.objects.get(mj_id=pk)
    serializer = manualjournalSerializer(instance=manualjournal, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#This Currently not used feature will be use Bulk updating time
#region

#RecJournal
@api_view(['GET'])


def recjournalCreation(request):
    recjournal = RecJournal.objects.all()   
    serializer = RecJournalSerializer(recjournal, many=True)
    return Response(serializer.data)

@api_view(['GET'])


def recjournalDetail(request, pk):
    recjournal = RecJournal.objects.get(rj_id=pk)
    serializer = RecJournalSerializer(recjournal, many=False)
    return Response(serializer.data)

@api_view(['POST'])


def recjournalUpdate(request, pk):
    recjournal = RecJournal.objects.get(rj_id=pk)
    serializer = RecJournalSerializer(instance=recjournal, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#BulkUpdate
@api_view(['GET'])


def bulkupdateCreation(request):
    bulkupdate = BulkUpdate.objects.all()   
    serializer = BulkUpdateSerializer(bulkupdate, many=True)
    return Response(serializer.data)

@api_view(['GET'])


def bulkupdateDetail(request, pk):
    bulkupdate = BulkUpdate.objects.get(bu_id=pk)
    serializer = BulkUpdateSerializer(bulkupdate, many=False)
    return Response(serializer.data)

@api_view(['POST'])


def bulkupdateUpdate(request, pk):
    bulkupdate = BulkUpdate.objects.get(bu_id=pk)
    serializer = BulkUpdateSerializer(instance=bulkupdate, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#Budget
@api_view(['GET'])
def budgetCreation(request):
    budget = Budget.objects.all()   
    serializer = BudgetSerializer(budget, many=True)
    return Response(serializer.data)

@api_view(['GET'])

def budgetDetail(request, pk):
    budget = Budget.objects.get(budget_id=pk)
    serializer = BudgetSerializer(budget, many=False)
    return Response(serializer.data)



@api_view(['POST'])

def budgetUpdate(request, pk):
    budget = Budget.objects.get(budget_id=pk)
    serializer = BudgetSerializer(instance=budget, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

from django.db import transaction
from rest_framework.views import APIView
class UpdateJournalView(APIView):

    def put(self, request, pk):
        mj_data = request.data
        user = request.user
        print(mj_data)

        return self.handle_update(user,mj_data,pk)
    @transaction.atomic
    def handle_update(self,user,mj_data,pk):
        journal_transactions = mj_data["journal_transactions"]
        total_credit = round(sum(float(transaction['credit']) for transaction in journal_transactions),2)
        total_debit = round(sum(float(transaction['debit']) for transaction in journal_transactions),2)
        print(total_debit,total_credit)
        if total_credit != total_debit:
            return Response({"message": "Journal total not matching"}, status=400)
        company_id = Company.objects.get(company_id=mj_data["company_id"])
        branch_id =  Branch.objects.get(branch_id=mj_data["branch_id"])
        journal = ManualJournal.objects.select_for_update().get(mj_id=pk)
        MasterTransaction.objects.filter(L1detail_id=journal.mj_id).delete()
        mj_serializers = manualjournalSerializer(journal, data=mj_data)
        if mj_serializers.is_valid():
            mj_serializers.save()
            msg = "Details Updated Successfully"
        else:
            return Response(mj_serializers.errors, status=400)
        mj_transaction = mj_data['journal_transactions']
        Audit.objects.create(
            company_id=company_id,
            branch_id=branch_id,
            modified_by=user,
            module="Journal",
            audit_modified_date=mj_data['journal_date'],
            sub_module="Journal",
            data=mj_data
        )
        for journal_transaction in mj_transaction:
            if journal_transaction['contact'] is not None:
                contact = journal_transaction['contact']
                customer = SalesCustomer.objects.filter(customer_id=contact)
                if customer.exists():
                    customer = customer[0]
                else:
                    customer = None
                vendor = None
                if customer is None:
                    vendor = Vendor.objects.filter(vendor_id=contact)
                    if vendor.exists():
                        vendor = vendor[0]
                    else:
                        vendor = None
            else:
                customer = None
                vendor = None
            FROM_COA = COA.objects.get(coa_id=journal_transaction["coa_id"])
            TO_COA = COA.objects.get(coa_id=journal_transaction["coa_id"])
            MasterTransaction.objects.create(
                L1detail_id=journal.mj_id,
                L1detailstbl_name='ManualJournal',
                main_module='Accounting',
                module='Accounting',
                sub_module='ManualJournal',
                transc_deatils='Manual Journal Transaction',
                banking_module_type='ManualJournal',
                journal_module_type='ManualJournal',
                trans_date=mj_data["journal_date"],
                trans_status='Manually Added',
                debit=journal_transaction["debit"],
                to_account=TO_COA.coa_id,
                to_acc_type=TO_COA.account_type,
                to_acc_head=TO_COA.account_head,
                to_acc_subhead=TO_COA.account_subhead,
                to_acc_name=TO_COA.account_name,
                credit=journal_transaction["credit"],
                from_account=FROM_COA.coa_id,
                from_acc_type=FROM_COA.account_type,
                from_acc_head=FROM_COA.account_head,
                from_acc_subhead=FROM_COA.account_subhead,
                from_acc_name=FROM_COA.account_name,
                company_id=company_id,
                branch_id=branch_id,
                customer_id=customer,
                vendor_id=vendor)
            items = journal_transaction.get('items', [])
            if items:
                if journal_transaction['debit'] > 0:
                    flow_type = 'INWARD'
                else:
                    flow_type = 'OUTWARD'

                by_stocks = Stock.objects.filter(
                    ref_id=journal.mj_id,
                    ref_tblname=journal_transaction["coa_id"],
                    branch_id=journal.branch_id,
                    company_id=journal.company_id,
                    flow_type=flow_type,
                )
                prev_stk_list = {
                    (stock.item_id, stock.batch_no, stock.expire_date, stock.mfg_date,float(stock.quantity),
                     float(stock.amount), stock.godown_id_id): stock for stock
                    in
                    by_stocks}
                by_stk_list = {}
                print(items,">>>>>>>>>")
                for item in items:
                    if item['debit'] > 0:
                        amt = float(item['debit'])
                        flow_type = 'INWARD'
                        stock_in = float(item['quantity'])
                        stock_out = 0
                    else:
                        amt = float(item['credit'])
                        flow_type = 'OUTWARD'
                        stock_out = float(item['quantity'])
                        stock_in = 0
                    mj_obj, created = Stock.objects.get_or_create(
                        item_id=item['item_id'],
                        item_name=item["item_name"],
                        flow_type=flow_type,
                        stock_in=stock_in,
                        stock_out=stock_out,
                        ref_id=journal.mj_id,
                        ref_tblname=journal_transaction["coa_id"],
                        formname='ManualJournal',
                        batch_no=item['batch_no'],
                        mfg_date=item['mfg_date'],
                        expire_date=item['expire_date'],
                        godown_id_id=item['godown_id'],
                        godown_name=item['godown_name'],
                        quantity=round(float(item['quantity']), 2),
                        amount=round(float(amt), 2),
                        branch_id=branch_id,
                        company_id=company_id,

                        stage='Add Stages',
                        module="ManualJournal"
                    )
                    mj_obj.module_date = journal.created_date
                    mj_obj.date = mj_data["journal_date"]
                    mj_obj.save()
                    by_stk_list[(
                    mj_obj.item_id, mj_obj.batch_no, mj_obj.expire_date,
                    mj_obj.mfg_date,float(mj_obj.quantity),float(mj_obj.amount) ,mj_obj.godown_id_id)] = mj_obj
                for key, obj in prev_stk_list.items():
                    if key not in by_stk_list:
                        print("deleting child")
                        obj.delete()
        serializer = JournalTransactionSerializer(journal)
        return Response(serializer.data,status=200)
class ManualJournalupdateViewsets(viewsets.ModelViewSet):  
        queryset = ManualJournal.objects.all()
        serializer_class = manualjournalSerializer



        @transaction.atomic
        def update(self, request, pk, *args, **kwargs):
            mj_data = request.data
            company_id=mj_data["company_id"]
            if company_id is not None:
                company_id=Company.objects.get(company_id=company_id)
            try:
                mj= ManualJournal.objects.get(mj_id=pk)
            except ManualJournal.DoesNotExist:
                pass

            mj_serializers = manualjournalSerializer(mj, data=mj_data)

            if mj_serializers.is_valid():
                    mj_serializers.save()
                    msg="Details Updated Successfully" 
                           
            else:
                    return Response(mj_serializers.errors, status=400)
            #Update Chart Of Account Updated in User Selction   
            coa_list=[]
            print(mj_data['journal_transactions'])
            for journal_transaction in mj_data['journal_transactions']:
                coa_id=journal_transaction['coa_id']
                debit=journal_transaction['debit']
                credit=journal_transaction['credit']
                coa_list.append(coa_id)
                print('coa_id',coa_id,)
                print('debit',debit,)
                print('credit',credit,)
                
                
            #Select the User In slected contact     
                if journal_transaction['selected_contact'] is not None:
                    cust=journal_transaction['selected_contact'].get('customer_id')
                    vend=journal_transaction['selected_contact'].get('vendor_id')
                    if cust is not None:
                        customer=SalesCustomer.objects.get(customer_id=cust)
                        print('OOOOO',customer)
                    else:
                        customer=None
                    if vend is not None:
                        vendor=Vendor.objects.get(vendor_id=vend)
                        print('QQQQQ',vendor)
                    else:
                        vendor=None
                else:
                    customer=None
                    vendor=None
                    
                #Update the transaction in Masater tansaction with respective journal
                try:
                    to_manual_mast=MasterTransaction.objects.get(L1detail_id=mj.mj_id,to_account=coa_id) 
                    to_manual_mast.credit=credit
                    to_manual_mast.debit=debit
                    to_manual_mast.save()
            
                except MasterTransaction.DoesNotExist:
                    
                    FROM_COA = COA.objects.get(coa_id=journal_transaction["coa_id"])
                    TO_COA= COA.objects.get(coa_id=journal_transaction["coa_id"])
                    coa_list.append(journal_transaction["coa_id"])
                    dnmast = MasterTransaction.objects.create(
                        L1detail_id=mj.mj_id,
                        L1detailstbl_name='ManualJournal',
                        main_module='Accounting',
                        module='Accounting',
                        sub_module='ManualJournal',
                        transc_deatils='Manual Journal Transaction',
                        banking_module_type='ManualJournal',
                        journal_module_type='ManualJournal',
                        trans_date=mj_data["journal_date"],
                        trans_status='Manually Added',
                        debit=journal_transaction["debit"],
                        to_account=TO_COA.coa_id,
                        to_acc_type=TO_COA.account_type,
                        to_acc_head=TO_COA.account_head,
                        to_acc_subhead=TO_COA.account_subhead,
                        to_acc_name=TO_COA.account_name,
                        credit=journal_transaction["credit"],
                        from_account=FROM_COA.coa_id,
                        from_acc_type=FROM_COA.account_type,
                        from_acc_head=FROM_COA.account_head,
                        from_acc_subhead=FROM_COA.account_subhead,
                        from_acc_name=FROM_COA.account_name,
                        company_id=company_id,
                        customer_id=customer,
                        vendor_id=vendor)
                    dnmast.save()
            topics = MasterTransaction.objects.filter(L1detail_id=mj.mj_id,).exclude(to_account__in=coa_list).delete()

            serializer = manualjournalSerializer(mj)
            return Response(serializer.data)


@api_view(['GET'])
@renderer_classes([JSONRenderer])

def getMJDetailsByserial(request, company_id,branch_id):
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    journal_serial = request.GET['serial']
    mjs = ManualJournal.objects.filter(company_id=company_id,
                                       branch_id=branch_id,
                                       journal_serial_no__icontains=journal_serial)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": mjs.count()
    }
    manualjournal = mjs[offset:offset + limit]
    response['results'] = JoinJournalTransSerializer(manualjournal, many=True).data
    return Response(response)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getMJDetailsByreference(request, company_id,branch_id):
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    journal_ref = request.GET['ref']
    mjs = ManualJournal.objects.filter(company_id=company_id,
                                       branch_id=branch_id,
                                       journal_ref_no__icontains=journal_ref)
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": mjs.count()
    }
    manualjournal = mjs[offset:offset + limit]
    response['results'] = JoinJournalTransSerializer(manualjournal, many=True).data
    return Response(response)