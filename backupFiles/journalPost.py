from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from .models import Company, JournalTransaction
from coa.models import COA
from salescustomer.models_old import SalesCustomer
from .models import ManualJournal, RecJournal, BulkUpdate, Budget
from .serializers import JoinJournalTransSerializer, JournalTransactionSerializer, manualjournalSerializer, RecJournalSerializer, BulkUpdateSerializer, BudgetSerializer, shortmanualjournalSerializer
from rest_framework.decorators import api_view

# Create your views here.
#POST journal_transactions
class journalViewSet(viewsets.ModelViewSet):
    queryset = JournalTransaction.objects.all()
    serializer_class = JournalTransactionSerializer

    def create(self, request, *args, **kwargs):
        journal_data = request.data
        print("journal_data", journal_data)
        journal_object=journal_data["journal_object"]
        comp_id = Company.objects.get(company_id=journal_data["company_id"])

        #manual journals fields        
        journal_id=ManualJournal.objects.create(journal_ref_no=journal_data["journal_ref_no"],
        journal_status=journal_data["journal_status"],
        journal_serial_no=journal_data["journal_serial_no"],
        notes=journal_data["notes"],
        journal_type=journal_data["journal_type"],
        is_journal_generated=journal_data["is_journal_generated"],
        sub_total=journal_data["sub_total"],
        total=journal_data["total"],
        journal_amount=journal_data["journal_amount"],         
        company_id = comp_id)
        journal_id.save()
        print("journal_object",journal_object,type(journal_object))        
        

        for i in range(len(journal_object)):
            
            #for j in range(len(3)):
            #a=journal_object[i][j]
            #coa_id=
            new_journal = JournalTransaction.objects.create(mj_id=journal_id,
            #account=journal_object[i]["account"],              
            coa_id = COA.objects.get(coa_id=journal_object[i]["coa_id"]),
            company_id = comp_id,
            #customer_id = SalesCustomer.objects.get(customer_id=journal_object[i]["customer_id"]),                          
            des=journal_object[i]["des"],
            credit=journal_object[i]["credit"],
            debit=journal_object[i]["debit"],
            #contact=journal_object[i]["customer_id"],            
            customer_id = SalesCustomer.objects.get(customer_id=journal_object[i]["contact"]))
            #contact="CodeRizeTechnology")
            #customer_id = SalesCustomer.objects.get(customer_id=journal_object[i]["customer_id"])
            #print("coa_id",type(coa_id))

            #print("account", journal_object[i]["coa_id"])
            # print("journal_id", journal_id)
            # print("des", journal_object[i]["des"])
            # print("credit", journal_object[i]["credit"])
            # print("debit", journal_object[i]["debit"])
            #print("contact", journal_object[i]["customer_id"])

            new_journal.save()
            print(i,"journal_transaction")

        serializer = JournalTransactionSerializer(new_journal) #browser
        #serializer = JoinJournalTransSerializer(new_journal)   #postman
        #serializer = JournalSerializer(journal_id)  
        return Response(serializer.data)

#ManualJournal
class manualjournalViewSet(viewsets.ModelViewSet):#provision to add data from API by providing HTML form also we can see posted data
    queryset = ManualJournal.objects.all()
    serializer_class = manualjournalSerializer

class manualjournalList(generics.ListAPIView):
    queryset = ManualJournal.objects.all()
    serializer_class = manualjournalSerializer

    @api_view(['GET']) #@api_view Allow to define function that match http methods
    def manualjournalCreation(request):
        manualjournal = ManualJournal.objects.all()    
        serializer = manualjournalSerializer(manualjournal, many=True)
        return Response(serializer.data)

#API POST for JournalTransaction
class journaltransactionViewSet(viewsets.ModelViewSet):
    queryset = JournalTransaction.objects.all()
    serializer_class = JournalTransactionSerializer

class journaltransactionList(generics.ListAPIView):
    queryset = JournalTransaction.objects.all()
    serializer_class = JournalTransactionSerializer

    @api_view(['GET']) #@api_view Allow to define function that match http methods
    def journaltransactionCreation(request):
        journaltransaction = JournalTransaction.objects.all()    
        serializer = JournalTransactionSerializer(journaltransaction, many=True)
        return Response(serializer.data)

    @api_view(['GET'])
    def  journaltransactionDetails(request, pk):
        journaltransaction = JournalTransaction.objects.get(mj_id=pk)
        serializer = JournalTransactionSerializer(journaltransaction, many=True)
        return Response(serializer.data)

    
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

#getshortDetails
@api_view(['GET'])
def shortmanualjournalDetails(request):
    manualjournal = ManualJournal.objects.all()   
    serializer = shortmanualjournalSerializer(manualjournal, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def manualjournalDetail(request, pk):
    manualjournal = ManualJournal.objects.get(mj_id=pk)
    serializer = manualjournalSerializer(manualjournal, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def manualjournalupdate(request, pk):
    manualjournal = ManualJournal.objects.get(mj_id=pk)
    serializer = manualjournalSerializer(instance=manualjournal, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

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

