from fileinput import filename
import imp
from pprint import pformat
import pandas as pd
import json
import datetime
from pathlib import Path
import os

from django.http import FileResponse
from audit.models import Audit
from django.db.models import Q
from rest_framework.response import Response

from rest_framework.views import APIView

from item.models.stock_model import Stock
from item.serializers.stock_serializers import StockSerializerWithRefID
from rest_framework import status

from purchase.serializers.Bill_Item_serializers import GSTReportsBillItemSerializer
from purchase.serializers.Bill_serializers import GSTReportsONLYBillSerializer
from purchase.serializers.DebitItem_serializers import GSTReportsDebitnoteItemSerializer
from purchase.serializers.Debitnote_serializers import GSTReportsONLYDebitnoteSerializer
import json
from django.db.models.functions import Cast
from report.serializers import AuditSerializer
from salescustomer.serializers.Pr_serializers import prshortbycompanySerializer

from salescustomer.serializers.Creditnote_serializers import GSTReportONLYCnSerializer
from salescustomer.serializers.Invoice_serializers import GSTReportsONLYInvoiceSerializer
from salescustomer.serializers.Credit_item_serializers import GSTReportsCnItemSerializer
from salescustomer.serializers.Invoice_item_serializers import GSTReportsInvoiceItemSerializer

from transaction.serializers import MasterTransactionSerializer
from transaction.models import MasterTransaction

from .printing import print_balance_sheet,print_balance_sheet_v1, convert_balance_sheet_response
from .generate_pnl import print_pnl_sheet,convert_profit_loss_response

from rest_framework.decorators import api_view, permission_classes,authentication_classes
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum, F,FloatField,ExpressionWrapper
# Create your views here.
# cnshortbycompanyid



@api_view(['GET'])
def cnshortbycompanyid(request, comp_id):
    company = Company.objects.get(company_id=comp_id)
    cn = CreditNote.objects.filter(company_id=company)
    serializer = creditnoteshortbycompanyserializer(cn, many=True)
    return Response(serializer.data)

# payment receive short by company id


@api_view(['GET'])
def prshortbycompanyid(request, comp_id):
    company = Company.objects.get(company_id=comp_id)
    paymentreceive = PR.objects.filter(company_id=company)
    serializer = prshortbycompanySerializer(paymentreceive, many=True)
    return Response(serializer.data)

# Invoice short by company id


@api_view(['GET'])
def invoiceshortbycompanyid(request, comp_id):
    #invoice = Invoice.objects.all()
    company = Company.objects.get(company_id=comp_id)
    invoice = Invoice.objects.filter(company_id=company)
    serializer = invoiceshortbycompanySerializer(invoice, many=True)
    return Response(serializer.data)

# Sales order short by company id


@api_view(['GET'])
def ShortSalesOrderDetails(request, comp_id):
    company = Company.objects.get(company_id=comp_id)
    so = SO.objects.filter(company_id=company)
    serializer = ShortSalesOrderSerializer(so, many=True)
    return Response(serializer.data)

# Delivery challan short by company id


@api_view(['GET'])
def dcshortbycompanyid(request, comp_id):
    company = Company.objects.get(company_id=comp_id)
    dc = DC.objects.filter(company_id=company)
    serializer = dcshortbycompanySerializer(dc, many=True)
    return Response(serializer.data)

# Estimate short by company id


@api_view(['GET'])
def ShortEstimateDetails(request, comp_id):
    company = Company.objects.get(company_id=comp_id)
    estimate = Estimate.objects.filter(company_id=company)
    serializer = ShortEstimateSerializer(estimate, many=True)
    return Response(serializer.data)

# billshortbycompanyid


@api_view(['GET'])
def billshortbycompanyid(request, comp_id):
    company = Company.objects.get(company_id=comp_id)
    billed = Bill.objects.filter(company_id=company)
    serializer = billshortbycompanySerializer(billed, many=True)
    return Response(serializer.data)




# dnshortbycompanyid


@api_view(['GET'])
def dnshortbycompanyid(request, comp_id):
    company = Company.objects.get(company_id=comp_id)
    dn = DebitNote.objects.filter(company_id=company)
    serializer = debitnoteshortSerializer(dn, many=True)
    return Response(serializer.data)

# get payment made short by company id


@api_view(['GET'])
def getpaymentmadeshortbycompanyid(request, comp_id):
   # paymentmade = PaymentMade.objects.all()#here if we use wrong object(company) then it will shows null values for all fields
    company = Company.objects.get(company_id=comp_id)
    paymentmade = PaymentMade.objects.filter(company_id=company)
    serializer = paymadeshortbycompanySerializer(paymentmade, many=True)
    return Response(serializer.data)

# get purchase order details by company id


@api_view(['GET'])
def getpurchaseordershortbycompanyid(request, comp_id):
    # po = PO.objects.all()#here if we use wrong object(company) then it will shows null values for all fields
    company = Company.objects.get(company_id=comp_id)
    po = PO.objects.filter(company_id=company)
    serializer = poshortbycompanySerializer(po, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def ershortbycompanyid(request, comp_id):
    #expenserecord = ExpenseRecord.objects.all()
    company = Company.objects.get(company_id=comp_id)
    expenserecord = ExpenseRecord.objects.filter(company_id=company)
    serializer = ExpenseDetailsSerializer(expenserecord, many=True)
    return Response(serializer.data)

#Rules of Profit and loss Section
def get_sum_by_profit_loss_rule(debit, credit, acc_type):
    
    if acc_type in ('Income'):
        value =  credit - debit
    elif acc_type == 'Expense':
        value = debit - credit
    else:
        raise Exception(f'Not a valid acc_type: {acc_type}')
        
    return round(value,2)
# rules of balnce sheat
def get_sum_by_rule(debit, credit, acc_type):
    
    if acc_type in ('Liabilities', 'Equity'):
        
        #if credit >debit:
            #checking if Credit is greter so that we can positive Value
        value= credit-debit
       # else:
            #credit is small then we will get negative value,
            #to avoid that we will make debit -credit
            #here we are in Liability account but due to negative value 
            #we have to set the account asset for this value while returning
        #     value=debit=credit
        
    elif acc_type == 'Assets':
        # if debit>credit:
        value=debit-credit
        # else:
             #debit is small then we will get negative value,
            #to avoid that we will make credit-debit 
            #here we are in Asset account but due to negative value 
            #we have to set the account liability for this value while returning
            # value=credit -debit
    else:
        raise Exception(f'Not a valid acc_type: {acc_type}')
    #To keep 2 decimal Places 
    return round(value,2)
#Chnage GST vlaues as Per Responce  output minus input
def chnages_responc_gst(responce):  
    Output_CGST=responce['data']['Liabilities & Equities']['Liabilities']['Current Liabilities']['Other Current Liabilities'].get('Output CGST')
    #Input_CGST=responce['data']['Assets']['Assets']['Current Assets']['Other Current Assets'].get('Input CGST')
    Input_CGST = responce['data'].get('Assets', {}).get('Assets', {}).get('Current Assets', {}).get('Other Current Assets', {}).get('Input CGST')
    Output_SGST=responce['data']['Liabilities & Equities']['Liabilities']['Current Liabilities']['Other Current Liabilities'].get('Output SGST')
    #Input_SGST=responce['data']['Assets']['Assets']['Current Assets']['Other Current Assets'].get('Input SGST')
    Input_SGST = responce['data'].get('Assets', {}).get('Assets', {}).get('Current Assets', {}).get('Other Current Assets', {}).get('Input SGST')
    try:
        Output_IGST=responce['data']['Liabilities & Equities']['Liabilities']['Current Liabilities']['Other Current Liabilities']['Input IGST']
        Input_IGST=responce['data']['Assets']['Assets']['Current Assets']['Other Current Assets']['Input IGST']
        responce['data']['Liabilities & Equities']['Liabilities']['Current Liabilities']['Other Current Liabilities']['Output IGST']=round(Output_IGST-Input_IGST,2)
    except KeyError:
        pass
    # if Output_CGST and Output_SGST is not None:
    #     responce['data']['Liabilities & Equities']['Liabilities']['Current Liabilities']['Other Current Liabilities']['Output CGST']=round(Output_CGST-Input_CGST,2)
    #     responce['data']['Liabilities & Equities']['Liabilities']['Current Liabilities']['Other Current Liabilities']['Output SGST']=round(Output_SGST-Input_SGST,2)
    # return responce
    if Output_CGST is not None and Input_CGST is not None:
        responce['data']['Liabilities & Equities']['Liabilities']['Current Liabilities']['Other Current Liabilities']['Output CGST'] = round(Output_CGST - Input_CGST, 2)

    if Output_SGST is not None and Input_SGST is not None:
        responce['data']['Liabilities & Equities']['Liabilities']['Current Liabilities']['Other Current Liabilities']['Output SGST'] = round(Output_SGST - Input_SGST, 2)

    return responce

#Group By Function Created By Nielsh Sir 

def makeGrouBySubHead(acc_dict):
    accountObject={}
    print("Response type is ",type(acc_dict))
    retvalue=accountObject
    #if acc_dict is list:
        
    acc=pd.DataFrame(acc_dict)
    accountObject=acc.groupby(['acc_type', 'acc_head', 'acc_subhead','account_name']).agg(
            { 'debit': 'sum',"credit":"sum"}).reset_index()
        
    accountObject=accountObject.to_dict(orient='records')
    #retvalue=[accountObject]
    return accountObject

class AuditView(APIView):
    def get(self, request,company_id=None,branch_id=None,start_date=None,end_date=None):

        limit = int(request.GET['limit'])
        offset = int(request.GET['offset'])
        module = request.GET['module']

        if end_date and start_date and company_id and branch_id and module:
            print(module)
            objs = Audit.objects.filter(
                Q(
                    branch_id=branch_id,
                    company_id=company_id,
                    module=module
                ) &
                (Q(audit_created_date__range=(start_date, end_date)) | Q(audit_modified_date__range=(start_date, end_date)))



            )
            url = str(request.build_absolute_uri()).split("?")[0]
            response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                        "count": objs.count()}
            objs = objs[offset:offset + limit]

            serializer = AuditSerializer(objs,many=True)
            response['results'] = serializer.data
            return Response(response,status=200)
        return Response(status=400)

class BalanceSheetView(APIView):
    def get(self,request, to_date, from_date, comp_id):
        pass

n_data=None
@api_view(['GET'])

#

def getbalancesheat_to_from_date(request, to_date, from_date, comp_id):
    try:

        output_excel=f"rep_{datetime.datetime.now().timestamp()}.xlsx"
        transactions = MasterTransaction.objects.filter(
            trans_date__range=(from_date, to_date), company_id=comp_id)
        
        # print("**************TRANSACTION IS*************",transactions)
        # gruop=transactions.aggregate(Sum('debit'),Sum('credit'))
        # print('""""""""""""""""""""',gruop)
        print(transactions.filter(from_acc_name="Input IGST"))
        if not transactions:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        df = pd.DataFrame(transactions.values('to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                          'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit'))
        # print("***************************df",df)
        # print("***************************df",df['credit'])
        # print("***************************df",df['debit'])
        df['amount'] = df['credit'] - df['debit']
        amount_total= df['amount'].sum()
        json_res = df.to_json(orient='columns')

        from_acc = df.groupby(['from_acc_type', 'from_acc_head', 'from_acc_subhead','from_acc_name',]).agg(
            {'credit': 'sum',}).reset_index()
        to_acc = df.groupby(['to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',]).agg(
            { 'debit': 'sum'}).reset_index()
        from_acc = from_acc.rename(columns={
                                   'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead','from_acc_name':'account_name','debit':'debit'}, inplace=False)
        to_acc = to_acc.rename(columns={
                               'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead','to_acc_name':'account_name','credit': 'credit'}, inplace=False)
        
        df_accounts = pd.concat([from_acc, to_acc])
        df_accounts.fillna(0, inplace=True)
        #print(df_accounts)
        
        # df_accounts.to_excel(f"media/reports/{output_excel}")
        output_path=os.path.join("media/excel",output_excel)
        if output_excel:
            http = 'https' if request.is_secure() else 'http'
            excel_url = f'https://auto-count-bucket.s3.amazonaws.com/media/reports/{output_excel}'
        else:
            excel_url = 'File Not found'
 
        # jsonRes = (df_accounts.to_json(orient='records'))
  
        response = json.loads(df_accounts.to_json(orient='records'))
        #this list is used to balance sheat data
        account_type_list=[]
        #this list is used to profit and loss
        account_type_list1=[]
        total_dict = {}
        #pl dictionary data
        total_dict1={}
        # featch the data maseter transaction to profit and loss section data
        
        #get the Groupby Databased on the Account subheads
        acc_groupby=makeGrouBySubHead(response)
        # print("Response",response)
        # print("Group BY",acc_groupby)
        for acc_type_object1 in acc_groupby:
            if acc_type_object1['acc_type'] in ('Expense','Income',):
                acc_type_object1['debitcredit'] = get_sum_by_profit_loss_rule(acc_type_object1['debit'], acc_type_object1['credit'], acc_type_object1['acc_type'])
                account_type_list1.append(acc_type_object1)
            else:
                continue
            # Calculate Total profit and loss
            valid_acc_types1 = ('Expense','Income')
            for valid_acc_type1 in valid_acc_types1:
                if acc_type_object1['acc_type'] == valid_acc_type1:
                    if f'{valid_acc_type1}_sum' not in total_dict1.keys():
                        total_dict1[f'{valid_acc_type1}_sum'] = 0 
                        
                    total_dict1[f'{valid_acc_type1}_sum'] += acc_type_object1['debitcredit']
        #account type list Added the data of Liabilites Assets and Equity
        #and return the three Type
        # print("Account is here after Group By***")
        # print("Account TYpe--- Head------SubHead----Debit----Credit")
        # print(makeGrouBySubHead(response))
        # print("Account is here ***")
        # print("Account TYpe--- Head------SubHead----Debit----Credit")
        # print('@@@',acc_groupby)
        for acc_type_object in acc_groupby:
            if acc_type_object['acc_type'] in ('Liabilities', 'Equity','Assets'):
                #print(acc_type_object['acc_type'],acc_type_object['acc_head'],acc_type_object['acc_subhead'],acc_type_object['debit'], acc_type_object['credit'])    
                #herer we need to check for Positive and negative values
                if acc_type_object['acc_type']=='Liabilities':
                    if acc_type_object['credit'] >acc_type_object['debit']:
                        
                  #checking if Credit is greter so that we can positive Value
                       
                        acc_type_object['debitcredit'] = get_sum_by_rule(acc_type_object['debit'], acc_type_object['credit'], acc_type_object['acc_type'])
                        print('WW',acc_type_object['acc_type'])
                        #print(acc_type_object['debitcredit'])
                    else:
                       
                        #it means ther is negative value in Liabilities in that case 
                        #make the account type as Asset
                        acc_type_object['acc_type']='Assets'
                        acc_type_object['debitcredit'] = get_sum_by_rule(acc_type_object['debit'], acc_type_object['credit'], acc_type_object['acc_type'])
                        print('MMM',acc_type_object['acc_type'])
                       #print( acc_type_object['debitcredit'])
                elif acc_type_object['acc_type']=='Equity':
                    if acc_type_object['credit'] >acc_type_object['debit']:
                        
                  #checking if Credit is greter so that we can positive Value
                        
                        acc_type_object['debitcredit'] = get_sum_by_rule(acc_type_object['debit'], acc_type_object['credit'], acc_type_object['acc_type'])
                        
                    else:
                       
                        #it means ther is negative value in Liabilities in that case 
                        #make the account type as Asset
                        acc_type_object['acc_type']='Assets'
                        acc_type_object['debitcredit'] = get_sum_by_rule(acc_type_object['debit'], acc_type_object['credit'], acc_type_object['acc_type'])
                        
                
                elif acc_type_object['acc_type']=='Assets':
                        if acc_type_object['debit'] >acc_type_object['credit']:
                        #checking if debit is greter so that we can positive Value
                            acc_type_object['debitcredit'] = get_sum_by_rule(acc_type_object['debit'], acc_type_object['credit'], acc_type_object['acc_type'])
                            print("xxx",acc_type_object)
                        else:
                            
                            #it means ther is negative value in Asset in that case 
                            #make the account type as Liabilities
                            acc_type_object['acc_type']='Liabilities'
                            acc_type_object['debitcredit'] =get_sum_by_rule(acc_type_object['debit'], acc_type_object['credit'], acc_type_object['acc_type'])
                            print('YYY',acc_type_object)
                else:       
                    acc_type_object['debitcredit'] = get_sum_by_rule(acc_type_object['debit'], acc_type_object['credit'], acc_type_object['acc_type'])
                    print('$$$$',acc_type_object)
                
                account_type_list.append(acc_type_object)
            else:
                continue
           
            # Calculate Total Balance Sheat
            valid_acc_types = ('Liabilities', 'Assets', 'Equity')
            
            for valid_acc_type in valid_acc_types:
                if acc_type_object['acc_type'] == valid_acc_type:
                    if f'{valid_acc_type}_sum' not in total_dict.keys():
                        total_dict[f'{valid_acc_type}_sum'] = 0
                        
                     
                    total_dict[f'{valid_acc_type}_sum'] += acc_type_object['debitcredit']
                    

        converted_response = convert_balance_sheet_response(input_response=account_type_list)
        serializer = MasterTransactionSerializer(transactions, many=True)
        n_data=serializer.data
        try:
            liabilities_sum = total_dict['Liabilities_sum']
        except KeyError:
            liabilities_sum = 0
            
        try:
            Equity_sum = total_dict['Equity_sum']
        except KeyError:
            Equity_sum = 0
            
        sum_labi_equity=liabilities_sum+Equity_sum
       
        #this section is  profit and  loss 
        try:
            income_sum = total_dict1['Income_sum']
        except KeyError:
            income_sum = 0
            
        try:
            expense_sum = total_dict1['Expenses_sum']
        except KeyError:
            expense_sum = 0
            
        
        profit_loss = round(income_sum - expense_sum,2)
        if profit_loss >= 0:
            profit = profit_loss
            loss = None
        else:
            profit = None
            loss = profit_loss 
        if profit == None:
            total_dict['Liabilities_Equity_sum']=sum_labi_equity + loss
        else:
            total_dict['Liabilities_Equity_sum']=sum_labi_equity + profit
        
        response = {
            # 'original_data': account_type_list
            'data': converted_response,
            'total': total_dict,
             'profit_loss':
                {
                    'profit': profit,
                    'loss': loss
                },
            'company': n_data,
            'report_url':excel_url,
            'company_name':Company.objects.get(company_id=comp_id).company_name
            }
        

        
        html = print_balance_sheet(response_data=response)
        return html
    except COA.DoesNotExist:
        return Response("Transaction Not Avilable")

#Profit And Loss Section
# region
# Get Account Type Equity 
n_data=None
@api_view(['GET'])


def getprofit_loss_to_from_date(request, to_date, from_date, comp_id):
    try:


        transactions = MasterTransaction.objects.filter(
            trans_date__range=(from_date, to_date), company_id=comp_id)
        print(transactions)
        # gruop=transactions.aggregate(Sum('debit'),Sum('credit'))
        # print('""""""""""""""""""""',gruop)
        df = pd.DataFrame(transactions.values('to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                          'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit'))
        print(df)
        if df.empty:
            return Response({"message":"No Transaction availabels"},status=400)
        df['amount'] = df['credit'] - df['debit']
        amount_total= df['amount'].sum()
        json_res = df.to_json(orient='columns')

        from_acc = df.groupby(['from_acc_type', 'from_acc_head', 'from_acc_subhead','from_acc_name',]).agg(
            {'credit': 'sum',}).reset_index()
        to_acc = df.groupby(['to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',]).agg(
            { 'debit': 'sum'}).reset_index()
        from_acc = from_acc.rename(columns={
                                   'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead','from_acc_name':'account_name','debit':'debit'}, inplace=False)
        to_acc = to_acc.rename(columns={
                               'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead','to_acc_name':'account_name','credit': 'credit'}, inplace=False)

        df_accounts = pd.concat([from_acc, to_acc])
        df_accounts.fillna(0, inplace=True)
        # print(df_accounts)
        print(df_accounts)
        # jsonRes = (df_accounts.to_json(orient='records'))


        response = json.loads(df_accounts.to_json(orient='records'))
        print(response)
        account_type_list=[]
        total_dict = {}
        #account type list Added the data of Liabilites Assets and Equity
        #and return the three Type
        for acc_type_object in response:
           
            if acc_type_object['acc_type'] in ('Expense','Income'):
                acc_type_object['debitcredit'] = get_sum_by_profit_loss_rule(acc_type_object['debit'], acc_type_object['credit'], acc_type_object['acc_type'])
                account_type_list.append(acc_type_object)
            else:
                continue
                
            
            
            
            # Calculate Total
            valid_acc_types = ('Expense','Income')
            for valid_acc_type in valid_acc_types:
                print(acc_type_object['acc_type'])
                if acc_type_object['acc_type'] == valid_acc_type:
                    if f'{valid_acc_type}_sum' not in total_dict.keys():
                        total_dict[f'{valid_acc_type}_sum'] = 0 
                        
                    total_dict[f'{valid_acc_type}_sum'] += acc_type_object['debitcredit']
        print(total_dict)
        converted_response = convert_profit_loss_response(input_response=account_type_list)

        serializer = MasterTransactionSerializer(transactions, many=True)
        n_data=serializer.data
        # a=total_dict['Income_sum']
        
        # Calculate proft and loss
        print(total_dict)
        if len(total_dict) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            income_sum = total_dict['Income_sum']
           
        except KeyError:
            income_sum = 0
            
        try:
            expense_sum = total_dict['Expenses_sum']
        except KeyError:
            expense_sum = 0
            
        
        profit_loss = income_sum - expense_sum
        if profit_loss >= 0:
            profit = profit_loss
            loss = None
        else:
            profit = None
            loss = profit_loss * -1
            
        if profit == None:
            total_dict['Income_sum']=income_sum + loss
            #total_dict['Expenses_sum']=0
        else:
           total_dict['Expenses_sum']=expense_sum + profit
           #total_dict['Income_sum']=0
        response = {
            # 'original_data': account_type_list,
            'data': converted_response,
            'total': total_dict,
            'profit_loss':
                {
                    'profit': profit,
                    'loss': loss
                },
            'company': n_data,
            
        }
        
        output_pdf = "PNL.pdf"   # f"BS_{datetime.datetime.now().timestamp()}.pdf"
        html = print_pnl_sheet(response_data=response, output_path=os.path.join("media/reports", output_pdf))
        return html
    except COA.DoesNotExist:
        return Response("Transaction Not Avilable")
#endregion
#End Of Profit And Loss Section

#test balancesheet Code
#region
@api_view(['GET'])


def newgetbalancesheat_to_from_date(request, to_date, from_date):
    try:
        transactions = MasterTransaction.objects.filter(
            trans_date__range=(from_date, to_date))
        # gruop=transactions.aggregate(Sum('debit'),Sum('credit'))
        # print('""""""""""""""""""""',gruop)
        df = pd.DataFrame(transactions.values('to_acc_type', 'to_acc_head', 'to_acc_subhead',
                          'from_acc_type', 'from_acc_subhead', 'from_acc_head', 'debit', 'credit'))
        json_res = df.to_json(orient='columns')

        from_acc = df.groupby(['from_acc_type', 'from_acc_head', 'from_acc_subhead']).agg(
            {'credit': 'sum', 'debit': 'sum'}).reset_index()
        to_acc = df.groupby(['to_acc_type', 'to_acc_head', 'to_acc_subhead']).agg(
            {'credit': 'sum', 'debit': 'sum'}).reset_index()
        from_acc = from_acc.rename(columns={
                                   'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead'}, inplace=False)
        to_acc = to_acc.rename(columns={
                               'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead'}, inplace=False)

        df_accounts = pd.concat([from_acc, to_acc])
        print(from_acc)
        print(to_acc)
        print('Addition of to accounts')
        print(df_accounts)
        # df_accounts=df_accounts.groupby(['to_acc_type','to_acc_head','to_acc_subhead']).agg({'credit':'sum','debit':'sum'}).reset_index()
        print("About to send Json Response")
        jsonRes = (df_accounts.to_json(orient='records'))
        print("Json Response")
        print(jsonRes)
        response = json.loads(df_accounts.to_json(orient='records'))
        # response_to=json.loads(to_acc.to_json(orient='records'))
        print('response', response)

        serializer = MasterTransactionSerializer(df, many=True)
        # import json
        return Response(response)
       # return Response(json.loads(json_res))
    except COA.DoesNotExist:
        return Response("Transaction Not Avilable")
    except Exception as e:
        return Response(str(e), status=404)
#endregion
@api_view(['GET'])

# 
def download_a_report(request, report_file):

    file_path =  os.path.join(Path(__file__).parent.parent,  'media', report_file)
    if not os.path.exists(file_path):
        return Response("File Not found", status=404)
    else:
        return FileResponse(open(file_path, 'rb'), as_attachment=True)


#All Journal Transaction View
n_data=None
@api_view(['GET'])

# 
# def getJRNLbyFormID(self,form_id):
#     form_mast = MasterTransaction.objects.filter(L1detail_id=form_id)
#     df = pd.DataFrame(form_mast.values('to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
#                          'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit'))
    

#     print(df)
#     from_acc = df.groupby(['from_acc_type', 'from_acc_head', 'from_acc_subhead','from_acc_name',]).agg(
#         {'credit': 'sum'}).reset_index()
#     to_acc = df.groupby(['to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',]).agg(
#         { 'debit': 'sum'}).reset_index()
#     from_acc = from_acc.rename(columns={
#                                 'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead','from_acc_name':'account_name'}, inplace=False)
#     to_acc = to_acc.rename(columns={
#                             'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead','to_acc_name':'account_name'}, inplace=False)


#     df_accounts = pd.concat([from_acc, to_acc])
#     response = json.loads(df_accounts.to_json(orient='records'))

#     serializer = MasterTransactionSerializer(form_mast, many=True)
#     n_data=serializer.data
#     all_response = {
#             # 'original_data': account_type_list,
#             'form_data': n_data,
#             'transaction': response,
#         }
#     return Response(all_response)
@api_view(['GET'])

def getJRNLbyFormID(request,form_id):
    form_mast = MasterTransaction.objects.filter(L1detail_id=form_id)
    df = pd.DataFrame(form_mast.values('to_acc_type', 'to_acc_head', 'to_acc_subhead', 'to_acc_name',
                                        'from_acc_type', 'from_acc_subhead', 'from_acc_head', 'from_acc_name', 'debit', 'credit'))

    # Define the columns to check
    columns_to_check = ['from_acc_type', 'from_acc_head', 'from_acc_subhead', 'from_acc_name', 'debit', 'credit',
                        'to_acc_type', 'to_acc_head', 'to_acc_subhead', 'to_acc_name']

    # Check if the columns exist and replace missing values with None
    for col in columns_to_check:
        if col not in df.columns:
            df[col] = None

    print("coming columns in dataframe",df.columns)
    
    #Check if 'credit' and 'debit' columns exist before aggregation
    if 'credit' in df.columns:
        from_acc = df.groupby(['from_acc_type', 'from_acc_head', 'from_acc_subhead', 'from_acc_name']).agg(
            {'credit': 'sum'}).reset_index()
    else:
        from_acc = pd.DataFrame(columns=['from_acc_type', 'from_acc_head', 'from_acc_subhead', 'from_acc_name', 'credit'])
    
    if 'debit' in df.columns:
        to_acc = df.groupby(['to_acc_type', 'to_acc_head', 'to_acc_subhead', 'to_acc_name']).agg(
            {'debit': 'sum'}).reset_index()
    else:
        to_acc = pd.DataFrame(columns=['to_acc_type', 'to_acc_head', 'to_acc_subhead', 'to_acc_name', 'debit'])
    
    from_acc = from_acc.rename(columns={
        'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead', 'from_acc_name': 'account_name'}, inplace=False)
    to_acc = to_acc.rename(columns={
        'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead', 'to_acc_name': 'account_name'}, inplace=False)

    print("FROM ACCOUNT DATA",from_acc)
    print("TO ACCOUNT DATA",to_acc)
    df_accounts = pd.concat([from_acc, to_acc])
    
    response = json.loads(df_accounts.to_json(orient='records'))

    serializer = MasterTransactionSerializer(form_mast, many=True)
    n_data = serializer.data
    all_response = {
        # 'original_data': account_type_list,
        'form_data': n_data,
        'transaction': response,
    }
    return Response(all_response)



   
    
    
    
    
# GST Reports
    
#GST Sales Reports
#GST Sales Reports means Output tax entries added in which forms jus like invoice item and credit note item
#CGST SGST and IGST Reports 
#Featching the entries with respective table company id through

@api_view(['GET'])


def getsales_gstreport_bycompanyid(request,to_date, from_date, comp_id):
    # company = Company.objects.get(company_id=comp_id)
    invoice_item=InvoiceItem.objects.filter(invoice_id__invoice_date__range=(from_date, to_date),invoice_id__company_id=comp_id).exclude(tax_name__isnull=True)
    cn_item=CreditItem.objects.filter(cn_id__cn_date__range=(from_date, to_date),cn_id__company_id=comp_id).exclude(tax_name__isnull=True)
    invoice_serializer = GSTReportsInvoiceItemSerializer(invoice_item, many=True)
    cr_serializer = GSTReportsCnItemSerializer(cn_item, many=True)
    return Response({'invoice':invoice_serializer.data,'credit_note':cr_serializer.data})
    
@api_view(['GET'])


def getsales_gst_bycompanyid(request, to_date, from_date, comp_id,branch_id):
    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
    objs = SalesGst.objects.filter(company_id=comp_id,
                                   branch_id=branch_id,
                                   date__range=(from_date,to_date))
    serializer = SalesGstSerializer(objs,many=True)
    return Response({'data' :serializer.data})
    
    
    
#GST Purchase Reports

#GST Purchase report menas Input Tax Entries added in which form menas 
#CGST SGST IGST Entires
# Featching the entries with respective table with company id through 
#BiLL and Debit note Gst Addde and reture Both Data In Api Heating 

@api_view(['GET'])


def getpurchase_gstreport_bycompanyid(request,to_date, from_date, comp_id):
    company = Company.objects.get(company_id=comp_id)
    bill_item=Bill_Item.objects.filter(bill_id__bill_date__range=(from_date, to_date),bill_id__company_id=company).exclude(tax_name__isnull=True)
    dn_item=DebitItem.objects.filter(dn_id__dn_date__range=(from_date, to_date),dn_id__company_id=company).exclude(tax_name__isnull=True)
    bill_serializer = GSTReportsBillItemSerializer(bill_item, many=True) 
    dn_serializer = GSTReportsDebitnoteItemSerializer(dn_item, many=True)
    
    return Response({'bill':bill_serializer.data,'debit_note':dn_serializer.data})

@api_view(['GET'])


def getpurchase_gst_bycompanyid(request, to_date, from_date, comp_id,branch_id):
    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
    objs = PurchaseGst.objects.filter(company_id=comp_id,
                                      branch_id=branch_id,
                                      date__range=(from_date,to_date))
    serializer = PurchasegstSerializer(objs,many=True)
    return Response({'data' :serializer.data})

# @api_view(['GET'])
# def get3B_gstreport_bycompanyid(request,to_date, from_date, comp_id):
#     company = Company.objects.get(company_id=comp_id)
#     invoice_item=InvoiceItem.objects.filter(invoice_id__invoice_date__range=(from_date, to_date),invoice_id__company_id=comp_id,invoice_id__payment_status='unpaid').exclude(tax_name__isnull=True)
#     cn_item=CreditItem.objects.filter(cn_id__cn_date__range=(from_date, to_date),cn_id__company_id=comp_id,cn_id__status='Open').exclude(tax_name__isnull=True)
#     invoice_serializer = GSTReportsInvoiceItemSerializer(invoice_item, many=True)
#     cr_serializer = GSTReportsCnItemSerializer(cn_item, many=True)
#     bill_item=Bill_Item.objects.filter(bill_id__bill_date__range=(from_date, to_date),bill_id__company_id=company,bill_id__payment_status='unpaid').exclude(tax_name__isnull=True)
#     dn_item=DebitItem.objects.filter(dn_id__dn_date__range=(from_date, to_date),dn_id__company_id=company,dn_id__status='Open').exclude(tax_name__isnull=True)
#     bill_serializer = GSTReportsBillItemSerializer(bill_item, many=True) 
#     dn_serializer = GSTReportsDebitnoteItemSerializer(dn_item, many=True)
 
    
#     return Response({'invoice':invoice_serializer.data,'credit_note':cr_serializer.data,'bill':bill_serializer.data,'debit_note':dn_serializer.data})

#GST 2B Reports Section
#Filter the data Invoice item and Credit note item payment Status it Cloased
#2Areport Invoice payment status paid and credit note paymetnt staus Closed return 
#seralize the data and return separte all the data
@api_view(['GET'])


def get2B_gstreport_bycompanyid(request,to_date, from_date, comp_id):
    company = Company.objects.get(company_id=comp_id)
    invoice_item=Invoice.objects.filter(invoice_date__range=(from_date, to_date),company_id=company,payment_status='paid')
    credit_item=CreditNote.objects.filter(cn_date__range=(from_date, to_date),company_id=company,status='Closed')
    creditnote_serializer = GSTReportONLYCnSerializer(credit_item, many=True)        
    invoice_serializer = GSTReportsONLYInvoiceSerializer(invoice_item, many=True)    
    return Response({'invoice':invoice_serializer.data,'credit_note':creditnote_serializer.data})


#GST 2A Reports Section
#2A Report means bill item statu is paid and debit item status close 
#filter the statusin bill item table
#serializea all data and return separte the data
@api_view(['GET'])


def get2A_gstreport_bycompanyid(request,to_date, from_date, comp_id):
    company = Company.objects.get(company_id=comp_id)
    bill_item=Bill.objects.filter(bill_date__range=(from_date, to_date),company_id=company,payment_status='paid')
    debit_item=DebitNote.objects.filter(dn_date__range=(from_date, to_date),company_id=company,status='Closed')
    debit_serializer = GSTReportsONLYDebitnoteSerializer(debit_item, many=True)        
    bill_serializer = GSTReportsONLYBillSerializer(bill_item, many=True)    
    return Response({'Bill':bill_serializer.data,'debitnote':debit_serializer.data})
   
   
# updated__gte=F('added_toSolr_date')
@api_view(['GET'])


def get3Bs_gstreport_bycompanyid(request,to_date, from_date, comp_id):
    company = Company.objects.get(company_id=comp_id)
    stock_item=Stock.objects.filter(date__range=(from_date, to_date),company_id=company, stock_out__gte=F('stock_in'))
    # for item in stock_item:
        # stock_in_item=item.stock_in
        # stock_out_item=item.stock_out
        # if stock_out_item >= stock_in_item:
        
    serializer = StockSerializerWithRefID(stock_item, many=True)
        
  
    return Response({'report':serializer.data})
            
import time

@api_view(['GET'])


def InvoiceExcelReport(request,comp_id,from_date,to_date,branch_id):

    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
    
    if to_date < from_date:
            return Response(f"From date {from_date} is less than to date {to_date}", status=400)
    start = time.time()
    invoice = Invoice.objects.filter(company_id=comp_id,
                                     branch_id=branch_id,
                                     invoice_date__range=(from_date, to_date))
    serializer = invoiceshortbycompanySerializer(invoice, many=True)
    output_excel=f"inv_{datetime.datetime.now().timestamp()}.xlsx"
    end = time.time()
    print(f"total query time {end-start}")

    return Response({'data':serializer.data,'url':f'https://auto-count-bucket.s3.amazonaws.com/media/reports/{output_excel}','status':200,})
            
#Download the Excel Invoice Report          
def download_Inv_Report_Excel(request, file_name):
    file_path = f"media/excel/{file_name}"     
    response = FileResponse(open( file_path,'rb'),as_attachment=True)                            
    return response
#Payment recived Excel Report
@api_view(['GET'])


def PMRecieveExcelReport(request,comp_id,from_date,to_date,branch_id):

    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
    #Filter date and Company id wise

    paymentreceive = PR.objects.filter(company_id=comp_id,branch_id=branch_id,payment_date__range=(from_date, to_date))

    serializer1=PrExlReportSerializer(paymentreceive,many=True)


    return Response({'data':serializer1.data,'status':200})

#Download in excel Payment Recived report
def download_PR_Report_Excel(request, file_name):
    file_path =os.path.join( f"media/excel/{file_name}"  )      
    response = FileResponse(open( file_path,'rb'),as_attachment=True)                            
    return response

#Bill excel Reports Section
@api_view(['GET'])


def BillExcelReport(request,comp_id,from_date,to_date,branch_id):

    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()


    billed = Bill.objects.filter(company_id=comp_id,branch_id=branch_id,bill_date__range=(from_date, to_date))
    serializer = billshortbycompanySerializer(billed, many=True)

    return Response({'data':serializer.data,'status':200})

#Download Bill excel report
def download_Bill_Report_Excel(request, file_name):
    file_path =os.path.join( f"media/excel/{file_name}"  )      
    response = FileResponse(open( file_path,'rb'),as_attachment=True)                            
    return response


#Payment Made Excel Report Download Section

@api_view(['GET'])


def PMExcelReport(request,comp_id,from_date,to_date,branch_id):

    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

    pm = PaymentMade.objects.filter(company_id=comp_id,
                                    branch_id=branch_id,
                                    payment_date__range=(from_date, to_date))
    serializer = paymadeshortbycompanySerializer(pm, many=True)


    return Response({'data':serializer.data,'status':200})

#Download Excel Pm this Function Call 
def download_PM_Report_Excel(request, file_name):
    file_path = f"media/excel/{file_name}"
    response = FileResponse(open( file_path,'rb'),as_attachment=True)                            
    return response






# @api_view(['GET'])
# def Checkinvoicestock(request,comp_id,from_date,to_date):
#     company = Company.objects.get(company_id=comp_id)
#     invoice= Invoice.objects.filter(company_id=company,created_date__date__range=(from_date, to_date))
    
#     inv_stock = Stock.objects.filter(ref_id=invoice.invoice_id)
    
#     if inv_stock is not None:
#         pass
#     else:
        
        
    
#Day Book Reports Means Trasction Date Report 
#Filter the Tras Date and Company id 
# All The Return With Respective date and Company   
@api_view(['GET'])


def getDayBookReportLbydate(self,comp_id,date,branch_id):

    form_mast = MasterTransaction.objects.filter(company_id=comp_id,
                                                 branch_id=branch_id,
                                                 trans_date=date)
    serializer = DaybookreportSerializer(form_mast, many=True)  
    return Response({'data':serializer.data})





#Cash Book Report Section
#Cash Book Report its basically check the Account type in Cash 
#Filter the Date and Account 
#Account type is Cash is Hard Code
#Return Cash Related all Data
@api_view(['GET'])


def getCashBookReportLbydate(self,comp_id,from_date,to_date):
    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
    account_type='Cash'
    company = Company.objects.get(company_id=comp_id)
    form_mast = MasterTransaction.objects.filter(company_id=company,trans_date__range=(from_date, to_date),from_acc_subhead=account_type)
    if form_mast is None:
         form_mast = MasterTransaction.objects.filter(company_id=company,trans_date__range=(from_date, to_date),to_acc_subhead=account_type)
        
        
    serializer = CashbookreportSerializer(form_mast, many=True)  
    return Response({'CashBokk_report':serializer.data})
    
    
@api_view(['GET'])


def getCashBookBydate(request, to_date, from_date, comp_id,branch_id):
    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
    objs = CashBook.objects.filter(company_id=comp_id,
                                   branch_id=branch_id,
                                   trans_date__range=(from_date,to_date))
    serializer = CashBookSerializer(objs,many=True)
    return Response({'data' :serializer.data})


@api_view(['GET'])


def getBankBookBydate(request, to_date, from_date, comp_id,branch_id):
    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
    objs = BankBook.objects.filter(company_id=comp_id,
                                   branch_id=branch_id,
                                   trans_date__range=(from_date,to_date))
    serializer = BankBookSerializer(objs,many=True)
    return Response({'data' :serializer.data})
from django.db.models import Q
@api_view(['GET'])

def getGSTR3bBydate(request, to_date, from_date, comp_id,branch_id):
    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    getGSTR3bBydate
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    objs = GSTR3B.objects.filter(company_id=comp_id,
                                 branch_id=branch_id,
                                 date__range=(from_date, to_date))

    i_total = objs.aggregate(igst_total=Sum('igst_total'))['igst_total']
    s_total =  objs.aggregate(sgst_total=Sum('sgst_total'))['sgst_total']
    objs = objs[offset:offset + limit]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": GSTR3B.objects.filter(company_id=comp_id, date__range=(from_date, to_date)).count(),
        "igst_total":i_total,
        "sgst_total":s_total,
        "cgst_total":s_total
    }

    serializer = GSTR3BSerializer(objs,many=True)
    response['results'] = serializer.data
    return Response(response)

@api_view(['GET'])

def getGSTR2aBydate(request, to_date, from_date, comp_id,branch_id):

    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    objs = GSTR2A.objects.filter(company_id=comp_id,
                                 branch_id=branch_id,
                                 date__range=(from_date, to_date))

    i_total = objs.aggregate(igst_total=Sum('igst_total'))['igst_total']
    s_total = objs.aggregate(sgst_total=Sum('sgst_total'))['sgst_total']
    objs = objs[offset:offset + limit]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": GSTR2A.objects.filter(company_id=comp_id, date__range=(from_date, to_date)).count(),
        "igst_total": i_total,
        "sgst_total": s_total,
        "cgst_total": s_total
    }


    serializer = GSTR2ASerializer(objs,many=True)
    response['results'] = serializer.data
    return Response(response)

@api_view(['GET'])

def getGSTR2bBydate(request, to_date, from_date, comp_id,branch_id):
    om_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    objs = GSTR2B.objects.filter(company_id=comp_id,
                                 branch_id=branch_id,
                                 date__range=(from_date, to_date))

    i_total = objs.aggregate(igst_total=Sum('igst_total'))['igst_total']
    s_total = objs.aggregate(sgst_total=Sum('sgst_total'))['sgst_total']
    objs = objs[offset:offset + limit]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": GSTR2B.objects.filter(company_id=comp_id, date__range=(from_date, to_date)).count(),
        "igst_total": i_total,
        "sgst_total": s_total,
        "cgst_total": s_total
    }

    serializer = GSTR2BSerializer(objs, many=True)
    response['results'] = serializer.data
    return Response(response)



@api_view(['GET'])


def getBankBookReportLbydate(self,comp_id,from_date,to_date):
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        account_type='Bank'
        company = Company.objects.get(company_id=comp_id)
        from_mast = MasterTransaction.objects.filter(company_id=company,trans_date__range=(from_date,to_date),from_acc_subhead=account_type)
        #fetach the data in Master transaction table
        print('@@@@@@',from_mast)
        to_mast = MasterTransaction.objects.filter(company_id=company,trans_date__range=(from_date,to_date),to_acc_subhead=account_type)
        all_transactions = from_mast | to_mast\
        #Dataframe Cretaing
        if  len(from_mast) > 0 :      
            from_df = pd.DataFrame(from_mast.values('L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                                'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit','transc_deatils','trans_date','trans_status'))
            print(from_df)
            from_acc = from_df.groupby(['L1detail_id','from_acc_type', 'from_acc_head', 'from_acc_subhead','from_acc_name','transc_deatils','trans_date','trans_status',]).agg(
            {'credit': 'sum'}).reset_index()
            from_acc = from_acc.rename(columns={'L1detail_id':'L1detail_id',
                                    'from_acc_type': 'acc_type', 'from_acc_head': 'acc_head', 'from_acc_subhead': 'acc_subhead','from_acc_name':'account_name','transc_deatils':'transc_deatils','trans_date':'trans_date','trans_status':'trans_status'}, inplace=False)
        
        else:
            from_acc = None
        #Applying Condtions
        if len(to_mast) > 0:
            to_df = pd.DataFrame(to_mast.values('L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name',
                                'from_acc_type', 'from_acc_subhead','from_acc_head','from_acc_name','debit', 'credit','transc_deatils','trans_date','trans_status'))
            print(to_df)
            to_acc = to_df.groupby(['L1detail_id','to_acc_type', 'to_acc_head', 'to_acc_subhead','to_acc_name','transc_deatils','trans_date','trans_status',]).agg(
                { 'debit': 'sum'}).reset_index()
            to_acc = to_acc.rename(columns={'L1detail_id':'L1detail_id',
                                    'to_acc_type': 'acc_type', 'to_acc_head': 'acc_head', 'to_acc_subhead': 'acc_subhead','to_acc_name':'account_name','transc_deatils':'transc_deatils','trans_date':'trans_date','trans_status':'trans_status'}, inplace=False)
        else:
            to_acc = None
        if from_acc is not None and to_acc is not None:
            df_accounts = pd.concat([from_acc, to_acc])
        elif from_acc is not None:
            df_accounts = from_acc
        elif to_acc is not None:
            df_accounts = to_acc
        else:
            return Response("Data not found", status=404)
        #Change the reponse 
        from_response = json.loads(df_accounts.to_json(orient='records',date_format='iso'))
        #creating the empty list
        change_from_responce=[]
        for i in from_response:
            a=i['trans_date']
            i['trans_date']=a[:10]
            print(a[:10])
            change_from_responce.append(i)
        from_serializer = MasterTransactionSerializer(from_mast, many=True)
        to_serializer= MasterTransactionSerializer(to_mast,many=True)
        from_data=from_serializer.data
        to_data=to_serializer.data
        all_response = {
                'from_data': from_data,
                'to_data':to_data,
                'transaction': change_from_responce,

                # 'to_transaction':to_response,
            }
        print('@@@',all_response)
        return HttpResponse((json.dumps(all_response, cls=DjangoJSONEncoder))) 


from django.db.models import Q
from django.db.models.functions import ExtractMonth
from salescustomer.models.Pr_model import PR
import time
from .models import Dashboard,DashboardTotal
from .serializers import *
from django.db.models import Sum
from .models import AccountReport

class ProfitLossReportView(APIView):


    def get(self, request, from_date, to_date, comp_id,branch_id=None):
        start = time.time()
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        objs = AccountReport.objects.filter(
            Q(company_id=comp_id, trans_date__range=(from_date, to_date)) &
            Q(account_type__in=['Expense', 'Income'])
        )
        for each in objs:
            print(each.total)
        objects = objs.values('account', 'account_head', 'account_subhead', 'account_type', 'account_name').annotate(
            total=Sum('total')).exclude(
            total=0
        )
        ttl = objs.values('account_type').annotate(type_total=Sum('total')).exclude(total=0)
        if not ttl:
            return Response({"message": "No Data Found for given range"}, status=200)


        result = {}

        dt = {}
        opening = 0
        inv_objs = ItemTransaction.objects.filter(
            company_id=comp_id, date__range=(from_date, to_date))
        print(inv_objs, branch_id, comp_id, to_date, from_date)
        inv_objs = inv_objs.aggregate(
            total=Sum('sum_last_transactions'))

        closing = float(inv_objs.get('total', 0))
        # closing += 256204.70
        # trans_obj = MasterTransaction.objects.filter(Q(
        #     company_id=comp_id,
        #
        #     trans_date__lte=to_date
        # ) & Q(
        #     Q(
        #         to_account=str(closing_stock.coa_id)
        #     )
        #     |
        #     Q(
        #         from_account=str(closing_stock.coa_id)
        #     )
        # )).order_by('trans_date','created_date').last()
        # if trans_obj:
        #     closing = trans_obj.credit
        # print(objects)
        for each in objects:
            if each['account_name'] == "Opening Stock" and each['account_head'] == "Opening Stock":
                if each['total'] > 0:
                    opening = each['total']
                    continue
            # if each['account_name'] == "Closing Stock" and each['account_head'] == "Closing Stock":
            #     if each['total'] > 0:
            #         closing = each['total']
            #     continue
            account_head = each['account_head']

            account_name = {'name': each['account_name'], 'total': each['total'],'coa_id':each['account']}
            account_subhead = each['account_subhead']
            if not account_head in dt:
                dt[account_head] = {account_subhead: [account_name], 'type': each['account_type']}
            else:
                account_subhead = each['account_subhead']
                if account_subhead in dt[account_head]:
                    dt[account_head][account_subhead].append(account_name)
                else:
                    dt[account_head][account_subhead] = [account_name]

        result['data'] = dt

        for each in ttl:
            result[each['account_type']] = each['type_total']
        difference = round(float(result.get('Income', 0)) - float(result.get('Expense', 0)) + closing,2)
        result['loss_profit'] = difference
        result['closing_stock'] = closing
        result['opening_stock'] = opening
        result['Income'] = result.get('Income',0)
        result['Expense'] = result.get('Expense', 0)
        end = time.time()
        print(result)
        print(f"query time {end - start}")
        return Response(result, status=200)
from django.db.models.functions import Coalesce
from coa.models import TransactionDetail
from item.models.stock_model import ItemTransaction
from transaction.models import MasterTransaction
class BalanceSheetReportView(APIView):


    def get(self, request, from_date, to_date, comp_id,branch_id=None):

        start = time.time()
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        if branch_id:
            objs = AccountReport.objects.filter(
                account_type__in=['Liabilities', 'Assets'],
                branch_id=branch_id,
                company_id=comp_id, trans_date__range=(from_date, to_date))
        else:

            objs = AccountReport.objects.filter(
                Q(account_type__in=['Liabilities', 'Assets'],
                company_id=comp_id, trans_date__range=(from_date, to_date))
                & ~Q(account_subhead='Stock',account_head='Current Assets')

            )

        objects = objs.values('account', 'account_head', 'account_subhead', 'account_type', 'account_name').annotate(
            total=Sum('total')).exclude(
            total=0
        )
        # ivnentory_values  = list(Item.objects.filter(company_id=comp_id).values_list('inventory_account',flat=True).distinct())
        # print(ivnentory_values)
        # coas = COA.objects.filter(coa_id__in=ivnentory_values)
        inv_objs = ItemTransaction.objects.filter(
                company_id=comp_id, date__range=(from_date, to_date))
        print(inv_objs,branch_id,comp_id,to_date,from_date)
        inv_objs = inv_objs.aggregate(
            total=Sum('sum_last_transactions'))
        total = 0
        if inv_objs.get('total',0):
            total = inv_objs.get('total',0)
        inventory_total = float(total)
        # inventory_total +=  256204.70
        dt = {}
        dt['Current Assets'] = {'type':"Assets"}
        dt['Current Assets']['Stock'] = [{'name': "Closing Stock", "total": inventory_total}]
        # closing_stock = COA.get_closing_account(comp_id)
        # for coa in coas:
        #     trans_obj = MasterTransaction.objects.filter(Q(
        #         company_id=comp_id,
        #
        #         trans_date__lte=to_date
        #     ) & Q(
        #         Q(
        #             to_acc_head='Current Assets',
        #             to_acc_subhead='Stock',
        #             to_acc_name=coa.account_name
        #         )
        #         |
        #         Q(
        #             from_acc_head='Current Assets',
        #             from_acc_subhead='Stock',
        #             from_acc_name=coa.account_name
        #         )
        #     )).order_by('trans_date','created_date').last()
        #
        #     if 'Current Assets' not in dt:
        #         dt['Current Assets'] = {'Stock':[],'type': 'Assets'}
        #     dt['Current Assets']['Stock'].append({'name':coa.account_name,"coa_id":str(coa.coa_id),"total":trans_obj.credit})
        #     inventory_total += float(trans_obj.credit)



        for each in objects:
            account_head = each['account_head']

            account_name = {'name': each['account_name'], 'total': each['total'],"coa_id":each['account']}
            account_subhead = each['account_subhead']
            if not account_head in dt:
                dt[account_head] = {account_subhead: [account_name], 'type': each['account_type']}

            else:
                account_subhead = each['account_subhead']

                if account_subhead in dt[account_head]:
                    dt[account_head][account_subhead].append(account_name)
                else:
                    dt[account_head][account_subhead] = [account_name]
        print(dt)

        ttl = objs.values('account_type').annotate(type_total=Sum('total'))

        if not ttl:
            return Response({"message": "No Data Found for given range"}, status=200)
        # serializer = AccountReportSerializer(objects, many=True)
        result = {}
        result['data'] = dt

        for each in ttl:

            result[each['account_type']] = float(each['type_total'])
            # p&L

        if 'Assets' in result:
            result['Assets'] += inventory_total
        else:
            result['Assets'] = inventory_total
        result['Assets'] = round( result['Assets'],2)
        if branch_id:
            objs = AccountReport.objects.filter(
                account_type__in=['Expense', 'Income'],
                branch_id=branch_id,
                company_id=comp_id, trans_date__range=(from_date, to_date))
        else:
            objs = AccountReport.objects.filter(
                Q( company_id=comp_id, trans_date__range=(from_date, to_date)) &
                Q(account_type__in=['Expense', 'Income'])

               )
        ttl = objs.values('account_type').annotate(type_total=Sum('total'))
        res = {}

        for each in ttl:
            res[each['account_type']] = round(each['type_total'],2)
        if not ttl:
            difference = 0
        else:
            difference = float(res.get('Income', 0)  - res.get('Expense', 0))

        result['earnings'] = difference + inventory_total
        result['Liabilities'] = result.get('Liabilities', 0) +  result['earnings']

        end = time.time()
        print(f"query time {end - start}")
        print(result)
        return Response(result, status=200)

class DashboardReportView(APIView):

    def get(self,request,company_id,):
        start = time.time()

        objs = Dashboard.objects.filter(company_id=company_id)
        obj_total = DashboardTotal.objects.filter(company_id=company_id)

        if not obj_total:
            return Response(status=200)
        obj_total = obj_total[0]

        ret = {'month': [0 for i in range(12)], 'profit_loss': [0 for i in range(12)], 'sales': [0 for i in range(12)],
         'purchase': [0 for i in range(12)], 'pr':[0 for i in range(12)], 'pm': [0 for i in range(12)]}
        if objs:
            for inst in objs:

                month = int(inst.month) - 1
                # print(inst.profit_loss,month)
                ret['profit_loss'][month] = inst.profit_loss
                ret['sales'][month] = inst.sales
                ret['purchase'][month] = inst.purchase
                ret['pr'][month] = inst.pr
                ret['pm'][month] = inst.pm
        end1 = time.time()

        data = {
            'profit_loss':ret['profit_loss'],
            "sales_purchase":{
                "invoice":ret['sales'],
                "purchase":ret['purchase'],
            },
            "payment_mr":{
                "pm":ret['pm'],
                "pr":ret['pr']
            },
            "cash_bank":obj_total.cash_bank,
            "amount_receivable":obj_total.amount_receivable,
            "amount_payables":obj_total.amount_payable,
            "invoice_count":obj_total.invoice_count,
            "bill_count":obj_total.bill_count
        }
        end = time.time()
        print(f"total time {end-start}")

        return Response(data,status=200)

class StockValuationReportView(APIView):

    def get(self,request,from_date,to_date,comp_id,branch_id):
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        objs = StockValuationReport.objects.filter(company_id=comp_id,
                                                   created_date__range=(from_date, to_date),
                                                   branch_id=branch_id)
        data =  StockValuationReportSerializer(objs, many=True).data
        return Response(data,status=200)