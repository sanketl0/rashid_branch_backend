
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from statement.serializers import *
from statement.tasks import parseStatement
from salescustomer.serializers.Pr_serializers import updtPRMSerializer
from coa.models import COA
from transaction.models import MasterTransaction
from salescustomer.models.Salescustomer_model import SalesCustomer
from salescustomer.models.Invoice_model import Invoice
from purchase.serializers.Paymentmade_serializers import PaymentmadeSerializerNew
from purchase.models.Vendor_model import Vendor
from django.db import transaction
from registration.models import Feature
from audit.models import Audit
def background_task(file, bank, id):
    parseStatement(file, bank, id)

class BankView(APIView):

    

    def get(self,request):
        data = Bank.objects.all()
        serializer = BankSerializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class FileUploadView(APIView):

    

    def get(self,request,company_id,filename=None,bank_name=None,branch_id=None):
        limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
        offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
        if filename and company_id:
            data = FileUpload.objects.filter(company_id=company_id,branch_id=branch_id,filename__icontains=filename)[offset:offset + limit]
        elif company_id and bank_name:
            data = FileUpload.objects.filter(company_id=company_id,branch_id=branch_id, bank_id__name__icontains=bank_name)[offset:offset + limit]
        elif company_id:
            data = FileUpload.objects.filter(company_id=company_id,branch_id=branch_id)[offset:offset + limit]
            # Build the response links for pagination
        else:
            return Response(status=400)

        url = str(request.build_absolute_uri()).split("?")[0]
        response = {
            'next': url + f"?limit={limit}&offset={offset + limit}",
            'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
            "count": FileUpload.objects.filter(company_id=company_id).count()
        }

        serializer = FileUploadSerializer(data=data, many=True)
        serializer.is_valid()
        response['results'] = serializer.data
        return Response(response)

    @transaction.atomic
    def post(self,request):
        count = Feature.objects.get(user_id=request.user.id).statement_remaining
        print(count, 'statements ')
        if count <= 0:
            return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)
        bank = request.data.pop('bank')
        bank_obj = Bank.objects.get(name=bank[0])
        data = request.data
        data['bank_id'] = bank_obj.bank_id
        data['user_id'] = request.user.id
        file = data['file']
        serializer = FileUploadSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        id = serializer.data['file_id']
        company = serializer.data['company_id']

        print(file,bank,id,company)
        # test.delay("hi")
        parseStatement(file, bank, id,company)
        # thread = threading.Thread(target=background_task,args=(file,bank,id))
        # thread.start()
        return Response({"message":"successful parsed"},status=status.HTTP_201_CREATED)


class TransactionOldView(APIView):

    

    def get(self,request,file_id=None):
        if file_id:
            file_obj = FileUpload.objects.get(file_id=file_id)
            data = file_obj.transactions.filter(paid=False)
            serializer = TransactionSerializer(data=data, many=True)
            serializer.is_valid()
            return Response(serializer.data)
        data = Transaction.objects.all()
        serializer = TransactionSerializer(data=data,many=True)
        serializer.is_valid()
        return Response(serializer.data)

    @transaction.atomic
    def post(self,request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class TransactionView(APIView):

    

    def get(self,request,file_id=None):
        limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
        offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

        # Build the response links for pagination
        url = str(request.build_absolute_uri()).split("?")[0]

        file_obj = FileUpload.objects.get(file_id=file_id)
        response = {
            'next': url + f"?limit={limit}&offset={offset + limit}",
            'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
            "count": file_obj.transactions.filter(paid=False).count()
        }
        data = file_obj.transactions.filter(paid=False)[offset:offset + limit]
        serializer = TransactionSerializer(data=data, many=True)
        serializer.is_valid()
        response['results'] = serializer.data
        return Response(response)

    @transaction.atomic
    def post(self,request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

class TransactionDetailView(APIView):

    

    def get(self, request, transaction_id=None):
        obj = Transaction.objects.get(transaction_id=transaction_id)
        data = obj.transaction_details.all()
        serializer = TransactionDetailSerializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    @transaction.atomic
    def post(self,request):
        print(request.data)
        serializer = TransactionDetailSerializer(data=request.data)
        valid = serializer.is_valid()
        print(serializer.errors)
        if valid:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MultiPaymentView(APIView):

    

    @transaction.atomic
    def post(self,request):
        data = request.data
        payments = data.get('payments',None)
        user = request.user
        if payments:
            serializers = updtPRMSerializer(data=payments,many=True)
            serializers.is_valid(raise_exception=True)
            print(serializers.errors)
            serializers.save()
            payment_id = []
            for index,ser in enumerate(serializers.data):
                From_Bank = COA.objects.get(coa_id=ser["coa_id"])

                account_receivable = COA.objects.get(company_id=ser['company_id'], account_subhead="Account Receivables",isdefault=True)
                customer_id = SalesCustomer.objects.get(customer_id=ser['customer_id'])
                company_id = Company.objects.get(company_id=ser['company_id'])
                branch_id = Branch.objects.get(branch_id=ser['branch_id'])
                payment_id.append(ser['pr_id'])
                Audit.objects.create(
                    company_id=company_id,
                    branch_id=branch_id,
                    created_by=user,
                    audit_created_date=ser["payment_date"],
                    module="ReconciliationPR",
                    sub_module='ReconciliationPR',
                    data=payments[index]
                )
                prmast = MasterTransaction.objects.create(
                    L1detail_id=ser['pr_id'],
                    L1detailstbl_name='PR',
                    L3detail_id=ser['invoice_id'],
                    L3detailstbl_name='invoice',
                    main_module='Sales',
                    module='Payment Recived',
                    sub_module='PR',
                    transc_deatils='Payment Received',
                    trans_date=ser["payment_date"],
                    banking_module_type='Customer Payment',
                    journal_module_type='Invoice Payment',
                    trans_status='Manually Added',
                    debit=ser["amount_received"],
                    to_account=From_Bank.coa_id,
                    to_acc_type=From_Bank.account_type,
                    to_acc_head=From_Bank.account_head,
                    to_acc_subhead=From_Bank.account_subhead,
                    to_acc_name=From_Bank.account_name,
                    credit=ser['amount_received'],
                    from_account=account_receivable.coa_id,
                    from_acc_type=account_receivable.account_type,
                    from_acc_head=account_receivable.account_head,
                    from_acc_subhead=account_receivable.account_subhead,
                    from_acc_name=account_receivable.account_name,
                    customer_id=customer_id,
                    branch_id=branch_id,
                    company_id=company_id)
                prmast.save()
                balance_amount = ser["balance_amount"]
                print(f"balance amount is {balance_amount}")
                if float(balance_amount) <= 0:
                    invoice_id = Invoice.objects.get(invoice_id=ser["invoice_id"])

                    invoice_id.payment_status = 'paid'
                    invoice_id.amount_due = ser["balance_amount"]
                    invoice_id.save()
                    print('invoice status updated to ', invoice_id.payment_status)
                else:
                    invoice_id = Invoice.objects.get(invoice_id=ser["invoice_id"])
                    print('invoice id of else', invoice_id)
                    invoice_id.amount_due = ser["balance_amount"]
                    invoice_id.payment_status = 'unpaid'
                    invoice_id.save()
                    print('invoice amount due updated to ', invoice_id.amount_due)
            statement_data = {
                "transaction_id":request.data.get("transaction_id"),
                "amount": request.data.get("amount"),
                "bill_id": request.data.get("bill_id",[]),
                "invoice_id": request.data.get("invoice_id",[]),
                "voucher_id": request.data.get("voucher_id", []),
                "payment_id": payment_id,
                "purchase_id": request.data.get("purchase_id", []),
            }
            statement_serializer = TransactionDetailSerializer(data=statement_data)
            statement_serializer.is_valid(raise_exception=True)
            statement_serializer.save()
            return Response(status=200)
        return Response(status=400)



class MultiPaymentMadeView(APIView):

    

    @transaction.atomic
    def post(self,request):
        data = request.data
        payments = data.get('payments',None)
        user = request.user
        if payments:
            serializers = PaymentmadeSerializerNew(data=payments,many=True)
            serializers.is_valid(raise_exception=True)
            print(serializers.errors)
            serializers.save()
            payment_id = []
            print(serializers.data)
            for index,ser in enumerate(serializers.data):
                From_Bank = COA.objects.get(coa_id=ser["paid_through"])
                print(ser['company_id'])
                account_payable = COA.objects.get(company_id=ser['company_id'], account_subhead='Account Payables',isdefault=True)
                vendor_id = Vendor.objects.get(vendor_id=ser['vendor_id'])
                company_id = Company.objects.get(company_id=ser['company_id'])
                branch_id = Branch.objects.get(branch_id=ser['branch_id'])

                Audit.objects.create(
                    company_id=company_id,
                    branch_id=branch_id,
                    created_by=user,
                    audit_created_date=ser["payment_date"],
                    module="ReconciliationPM",
                    sub_module='Reconciliation',
                    data=payments[index]
                )
                payment_id.append(ser['pm_id'])
                prmast = MasterTransaction.objects.create(
                    L1detail_id=ser['pm_id'],
                    L1detailstbl_name='Payment Made',
                    L3detail_id=ser['bill_id'],
                    L3detailstbl_name='Bill',
                    main_module='Purchase',
                    module='Purchase',
                    sub_module='Payment Made',
                    transc_deatils='Payment Made',
                    trans_date=ser["payment_date"],
                    banking_module_type='Vendor Payment',
                    journal_module_type='Bill Payment',
                    trans_status='Manually Added',
                    debit=ser["amount_payable"],
                    to_account=account_payable.coa_id,
                    to_acc_type=account_payable.account_type,
                    to_acc_head=account_payable.account_head,
                    to_acc_subhead=account_payable.account_subhead,
                    to_acc_name=account_payable.account_name,
                    credit=ser['amount_payable'],
                    from_account=From_Bank.coa_id,
                    from_acc_type=From_Bank.account_type,
                    from_acc_head=From_Bank.account_head,
                    from_acc_subhead=From_Bank.account_subhead,
                    from_acc_name=From_Bank.account_name,
                    vendor_id=vendor_id,
                    branch_id=branch_id,
                    company_id=company_id)
                prmast.save()
                balance_amount = ser["balance_amount"]
                print(f"balance amount is {balance_amount}")
                bill_id = Bill.objects.get(bill_id=ser["bill_id"])
                if float(balance_amount) <= 0:

                    bill_id.payment_status = 'paid'
                    bill_id.amount_due = ser["balance_amount"]
                    bill_id.save()
                    print('bill status updated to ', bill_id.payment_status)
                else:
                    bill_id.payment_status = 'unpaid'
                    print('bill id of else', bill_id)
                    bill_id.amount_due = ser["balance_amount"]
                    bill_id.save()
                    print('bill amount due updated to ', bill_id.amount_due)

            statement_data = {
                "transaction_id":request.data.get("transaction_id"),
                "amount": request.data.get("amount"),
                "bill_id": request.data.get("bill_id",[]),
                "invoice_id": request.data.get("invoice_id",[]),
                "voucher_id": request.data.get("voucher_id", []),
                "payment_id":  request.data.get("payment_id", []),
                "purchase_id": payment_id,
            }

            statement_serializer = TransactionDetailSerializer(data=statement_data)
            statement_serializer.is_valid(raise_exception=True)
            statement_serializer.save()
            return Response(status=200)
        return Response(status=400)