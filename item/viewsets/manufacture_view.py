from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from item.models.manufacturing_journal import *
from item.serializers.manufature_serializer import *
from item.models.item_model import Item
from item.models.stock_model import *
import traceback
from django.db.models import Q
from audit.models import Audit
import traceback
from rest_framework.decorators import api_view

@api_view(['GET'])
def getManufactureBySerial(request, branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    serial = request.GET['serial']
    objs = ManufacturingJournal.objects.filter(mfg_serial_no__icontains=serial,
                                               branch_id=branch_id)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": objs.count()}
    objs = objs[offset:offset + limit]
    serializer = MfgManySerializer(objs, many=True)
    response['results'] = serializer.data
    return Response(response)

@api_view(['GET'])
def getManufactureByName(request, branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    name = request.GET['name']
    objs = ManufacturingJournal.objects.filter(item_name__icontains=name,
                                               branch_id=branch_id)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": objs.count()}
    objs = objs[offset:offset + limit]
    serializer = MfgManySerializer(objs, many=True)

    response['results'] = serializer.data

    return Response(response)
class StockJournalView(APIView):

    def get(self,request,company_id=None,branch_id=None,pk=None):
        if pk:
            obj = StockJournal.objects.get(sj_id=pk)
            serializer = StockJournalGetSerializer(obj)
            return Response(serializer.data,status=200)
        else:
            limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
            offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
            url = str(request.build_absolute_uri()).split("?")[0]
            objs = StockJournal.objects.filter(company_id=company_id, branch_id=branch_id)
            response = {
                'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": objs.count()
            }
            objs = objs[offset:offset + limit]
            response['results'] = StockJournalManySerializer(objs, many=True).data
            return Response(response)

    def handle_post(self,user, data):
        with transaction.atomic():
            try:
                serializer = StockJournalSerializer(data=data)
                user_id = user.id
                if serializer.is_valid():
                    obj = serializer.save()
                    obj.created_by = user_id
                    obj.save()
                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                company_id = Company.objects.get(company_id=data["company_id"])
                branch_id = Branch.objects.get(branch_id=data["branch_id"])
                Audit.objects.create(
                    company_id=company_id,
                    branch_id=branch_id,
                    created_by=user,
                    audit_created_date=data['date'],
                    module="Stock Journal",
                    sub_module="Stock Journal",
                    data=data
                )

            except Exception as e:
                traceback.print_exc()

                transaction.set_rollback(True)
                return Response({"message": str(e)}, status=400)

        return Response(status=201)

    def post(self,request):
        data = request.data
        user = request.user

        return self.handle_post(user,data)

    def handle_update(self, user,data, pk):
        with transaction.atomic():
            try:

                stk = StockJournal.objects.select_for_update().get(sj_id=pk)

                stk.consumption_items.all().delete()
                stk.production_items.all().delete()
                # Stock.objects.filter(ref_id=stk.sj_id).delete()
                MasterTransaction.objects.select_for_update().filter(L1detail_id=stk.sj_id).delete()
                serializer = StockJournalSerializer(stk,data=data)
                user_id = user.id
                if serializer.is_valid():
                    obj = serializer.save()
                    obj.modified_by = user_id
                    obj.save()
                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                company_id = Company.objects.get(company_id=data["company_id"])
                branch_id = Branch.objects.get(branch_id=data["branch_id"])
                Audit.objects.create(
                    company_id=company_id,
                    branch_id=branch_id,
                    modified_by=user,
                    audit_modified_date=data['date'],
                    module="Stock Journal",
                    sub_module="Stock Journal",
                    data=data
                )

            except Exception as e:
                traceback.print_exc()
                print(e)
                transaction.set_rollback(True)
                return Response({"message": str(e)}, status=400)

        return Response(status=201)

    def put(self,request,pk=None):
        if pk:
            data = request.data
            user = request.user
            return self.handle_update(user,data,pk)
class ManufactureView(APIView):

    def get(self,request,company_id=None,branch_id=None,pk=None):
        if pk:
            obj = ManufacturingJournal.objects.get(mfg_id=pk)
            serializer = MfgGetSerializer(obj)
            return Response(serializer.data,status=200)
        else:
            limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
            offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
            url = str(request.build_absolute_uri()).split("?")[0]
            objs = ManufacturingJournal.objects.filter(company_id=company_id, branch_id=branch_id)
            response = {
                'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": objs.count()
            }
            objs = objs[offset:offset + limit]
            response['results'] = MfgManySerializer(objs, many=True).data
            return Response(response)

    def handle_post(self,user, data):
        with transaction.atomic():
            try:
                serializer = MfgSerializer(data=data)
                serializer = MfgSerializer(data=data)
                user_id = user.id
                if serializer.is_valid():
                    obj = serializer.save()
                    obj.created_by = user_id
                    obj.save()
                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                company_id = Company.objects.get(company_id=data["company_id"])
                branch_id = Branch.objects.get(branch_id=data["branch_id"])
                Audit.objects.create(
                    company_id=company_id,
                    branch_id=branch_id,
                    created_by=user,
                    audit_created_date=data['journal_date'],
                    module="Manufacture",
                    sub_module="Manufacture",
                    data=data
                )

            except Exception as e:
                traceback.print_exc()

                transaction.set_rollback(True)
                return Response({"message": str(e)}, status=400)

        return Response(status=201)

    def post(self,request):
        data = request.data
        user = request.user

        return self.handle_post(user,data)

    def handle_update(self, user,data, pk):
        with transaction.atomic():
            try:
                mfg = ManufacturingJournal.objects.select_for_update().get(mfg_id=pk)
                mfg.mfg_items.select_for_update().all().delete()
                mfg.mfg_by_items.select_for_update().all().delete()
                # Stock.objects.select_for_update().filter(ref_id=mfg.mfg_id).delete()
                MasterTransaction.objects.select_for_update().filter(L1detail_id=mfg.mfg_id).delete()
                serializer = MfgSerializer(mfg,data=data)
                user_id = user.id
                if serializer.is_valid():
                    obj = serializer.save()
                    obj.modified_by = user_id
                    obj.save()
                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                company_id = Company.objects.get(company_id=data["company_id"])
                branch_id = Branch.objects.get(branch_id=data["branch_id"])
                Audit.objects.create(
                    company_id=company_id,
                    branch_id=branch_id,
                    modified_by=user,
                    audit_modified_date=data['journal_date'],
                    module="Manufacture",
                    sub_module="Manufacture",
                    data=data
                )

            except Exception as e:
                traceback.print_exc()
                print(e)
                transaction.set_rollback(True)
                return Response({"message": str(e)}, status=400)

        return Response(status=201)

    def put(self,request,pk=None):
        if pk:
            data = request.data
            user = request.user
            return self.handle_update(user,data,pk)
