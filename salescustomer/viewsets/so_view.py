import imp
import os
import json 
import uuid
from pathlib import Path
from io import BytesIO
import datetime
from rest_framework import viewsets,generics,mixins
from rest_framework.response import Response
from company.models import Company, Branch
from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.views.generic import View
from rest_framework.decorators import api_view
from salescustomer.printing.generate_so import generate_so_pdf
from utility import render_to_pdf,save_attach_file

from company.serializers import CompanySerializer
from salescustomer.models.Employee_model import Employee
from salescustomer.models.Tcs_model import TCS
from salescustomer.models.Salescustomer_model import SalesCustomer
from transaction.models import MasterTransaction
from item.models.item_model import Item
from salescustomer.models.So_item_model import SoItem
from salescustomer.serializers.So_item_serializers import SoItemSerializer,SOITEMSerializerUpdate
from salescustomer.models.So_model import SO
from salescustomer.serializers.So_serializers import (SOSerializer,JoinSoItemSerializer,ShortSalesOrderSerializer,
                                                      SalesOrderSerializerUpdate,SalesOrderShortByCompany_idSerializer)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from salescustomer.models.Estimate_model import Estimate
from coa.models import COA
from salescustomer.serializers.Salescustomer_serializers import SalesCustomerSerializer
#Sales Order Creation Section
from django.db import transaction
from registration.models import Feature
class salesorderitemsViewSet(viewsets.ModelViewSet):
    queryset = SoItem.objects.all()
    serializer_class = SoItemSerializer

    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        count = Feature.objects.get(user_id=request.user.id).so_remaining
        print(count, 'sales order')
        if count <= 0:
            return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)
        so_data_converte = request.data['data']
        print("#################################################")
        print(so_data_converte)
        print("salesorderData Format is ", type(so_data_converte))
        print("#################################################")
        # Salesorder Convert Str to Dict Code
        saleorder_data = json.loads(so_data_converte)
        print("Converted Format is", type(saleorder_data))

        so_file_data = request.FILES.get('attach_file')
        print("saleorder_data", type(so_file_data))
        print(saleorder_data)
        # return Response(status=200)
        try:
            employee_id = saleorder_data["emp_id"]
            if employee_id is not None:
                employee_id = Employee.objects.get(emp_id=employee_id)
        except KeyError:
            employee_id=None

        # pay_id=saleorder_data["payment_id"]
        # if pay_id is not None:
        #     pay_id=PaymentTerms.objects.get(payment_id=pay_id)

        try:    
            tcs_id = saleorder_data["tcs_id"]
            if tcs_id is not None:
                tcs_id = TCS.objects.get(tcs_id=tcs_id)
        except KeyError:
            tcs_id=None
        
        try: 
            branch_id = saleorder_data["branch_id"]
            if branch_id is not None:
                branch_id = Branch.objects.get(branch_id=branch_id)
        except KeyError:
            branch_id=None

        so_items = saleorder_data["so_items"]
        comp_id = Company.objects.get(company_id=saleorder_data["company_id"])
        # branch_id = Branch.objects.get(branch_id=estimate_data["branch_id"])
        cust_id = SalesCustomer.objects.get(
            customer_id=saleorder_data["customer_id"])

        # Sales order fields
        salesorder_id = SO.objects.create(so_ref_no=saleorder_data["so_ref_no"],
                                          so_date=saleorder_data["so_date"],
                                          so_status=saleorder_data["so_status"],
                                          so_serial=saleorder_data["so_serial"],
                                          is_so_generated=saleorder_data["is_so_generated"],
                                          attach_file=so_file_data,
                                          customer_note=saleorder_data["customer_note"],
                                          discount=saleorder_data["discount"],
                                          no_of_days=saleorder_data["no_of_days"],
                                          entered_discount=saleorder_data["entered_discount"],
                                          entered_shipping_charges=saleorder_data["entered_shipping_charges"],
                                          shipping_charges=saleorder_data["shipping_charges"],
                                          shipping_tax_name=saleorder_data["shipping_tax_name"],
                                          shipping_tax_rate=saleorder_data['shipping_tax_rate'],
                                          # subject=saleorder_data["subject"],
                                          supply_place=saleorder_data["supply_place"],
                                          terms_condition=saleorder_data["terms_condition"],
                                          total_gst=saleorder_data["total_gst"],
                                          term_name=saleorder_data["term_name"],
                                          expected_shipment_date=saleorder_data["expected_shipment_date"],
                                          sub_total=saleorder_data["sub_total"],
                                          total=saleorder_data["total"],
                                          cgst_total=saleorder_data['cgst_total'],
                                          sgst_total=saleorder_data['sgst_total'],
                                          igst_total=saleorder_data['igst_total'],
                                          company_id=comp_id,
                                          branch_id=branch_id,
                                          customer_id=cust_id,
                                          tcs_id=tcs_id,
                                          is_converted=saleorder_data['is_converted'],
                                          # payment_id = pay_id,
                                          emp_id=employee_id)
        salesorder_id.save()
        #
        if salesorder_id. is_converted == True:
            print("*********************",salesorder_id. is_converted)
        
          #  Assign the relevant fields from the estimate object to the sales order object:            
            salesorder_id.From_convt_id=saleorder_data['convt_id']
            salesorder_id.From_convt_ref_no=saleorder_data['convt_ref_no']
            salesorder_id.From_convt_serial=saleorder_data['convt_serial']
            salesorder_id.From_is_converted=saleorder_data["is_converted"]
            print("////////////////////////////////////////",salesorder_id.From_is_converted)
            salesorder_id.From_convt_type=saleorder_data['convt_type']
            salesorder_id.save() 
        
            print("OHHHHHHHHHHHHHHHHH")
            
            
            print("OHHHHHHHHHHHHHHHHH")
            
           # salesorder_id.save()   
            #get estimate by converted id 
            est= Estimate.objects.get(est_id=saleorder_data['convt_id'])
            print("sales order Object is Here ",salesorder_id.From_convt_id)
            print(est.To_is_converted)
            print("is conveted ****************")
            if est.To_is_converted==False:
                est.To_convt_id=salesorder_id.From_convt_id
                est.To_convt_ref_no=salesorder_id.From_convt_ref_no
                est.To_convt_serial=salesorder_id.From_convt_serial
                est.To_is_converted=salesorder_id.From_is_converted
                est.To_convt_type=salesorder_id.From_convt_type
                est.save()
            else:
                return Response({"message":"This Estimate Already Converted"},status=200)


        for i in range(len(so_items)):
            new_soitem = SoItem.objects.create(so_id=salesorder_id,
                                               item_id=Item.objects.get(
                                                   item_id=so_items[i]["item_id"]),
                                               # customer_id = SalesCustomer.objects.get(customer_id=estimate_items[i]["customer_id"],
                                               item_name=so_items[i]["item_name"],
                                               rate=so_items[i]["rate"],
                                               quantity=so_items[i]["quantity"],
                                               tax_rate=so_items[i]["tax_rate"],
                                               tax_name=so_items[i]["tax_name"],
                                               tax_type=so_items[i]["tax_type"],
                                               taxamount=so_items[i]["taxamount"],
                                               cgst_amount=so_items[i]['cgst_amount'],
                                               sgst_amount=so_items[i]['sgst_amount'],
                                               igst_amount=so_items[i]['igst_amount'],
                                               amount=so_items[i]["amount"],
                                               coa_id=COA.objects.get(
                                                   coa_id=so_items[i]["coa_id"]),)
            new_soitem.save()
            print(i, "so_items")

        serializer = SoItemSerializer(new_soitem)  # browser
        return Response(serializer.data)


########################################################

# Dwonload Code Is Creting api By Download
# Download salesorder by id




class SalesorderFileDownloadListAPIView(generics.ListAPIView):

    def get(self, request, salesorder_id, format=None):
        queryset = SO.objects.get(so_id=salesorder_id)
        if queryset.attach_file:
            file_handle = queryset.attach_file.path
            if os.path.exists(file_handle):
                document = open(file_handle, 'rb')
                response = HttpResponse(FileWrapper(
                    document), content_type='application/msword')
                response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.attach_file.name
                return response
            else:
                return HttpResponse("File Not Found")
        else:
            return HttpResponse('No File Found')


###################################################

#Sales Oreder Pdf generate Section
class SalesorderGeneratePdf(View):
    def get(self, request, salesorder_id, *args, **kwargs):
        so = SO.objects.get(so_id=salesorder_id)
        # Get The Estimate By estimate id
        # and Then Serialize the data
        serializer = SOSerializer(so)
        print(serializer.data)
        # get the Company data In Estimate (company_id) related
        print(so.company_id.company_id)
        company = Company.objects.get(company_id=so.company_id.company_id)
        # Serialize the data in Comapny
        company_serializer = CompanySerializer(company)
        print("##################################")
        print(serializer.data)
        print("##################################")
        print("Company Data", company_serializer.data)
        print("##################################")
        template = get_template('invoice.html')
        # Create the empty Dictionary in
        context = dict()
        # Add the Company and Invoice Data in Dictionary (Means Combine the data)
        context.update(dict(serializer.data))
        context.update(dict(company_serializer.data))
        html = template.render(context)

        return HttpResponse(html)


#####################

#Sales Order pdf download 
class SalesorderDownloadPdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        pdf_path = render_to_pdf('invoice.html')

        filename = "salesorder_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)

        # rendering the template

        with open(pdf_path, 'r') as f:
            file_data = f.read()

        # sending response
        response = FileResponse(file_data, as_attachment=True,
                                filename='hello.pdf', content_type='application/pdf')
        response['Content-Disposition'] = content
        return response


#############################################################
#############################################################
###############################################################3##########################


# api for get bill by company id and bill id
@api_view(['GET'])

# 
def download_so_data(request, so_id):

    # here filter the object of bill id and company id
    sls = SO.objects.select_related('customer_id','company_id').get(so_id=so_id)
    serializers = JoinSoItemSerializer(sls)

    html = generate_so_pdf(data=serializers.data)
    return html

def download_so(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'),as_attachment=True)
    #response = FileResponse(file_data, as_attachment=True,                              
    return response




#Sales Order 
class soViewSet(viewsets.ModelViewSet):
    queryset = SO.objects.all()
    serializer_class = SOSerializer

    

class soList(generics.ListAPIView):
    queryset = SO.objects.all()
    serializer_class = SOSerializer

    
    # @api_view Allow to define function that match http methods
    @api_view(['GET'])
    def soCreation(request):
        so = SO.objects.all()
        serializer = SOSerializer(so, many=True)
        return Response(serializer.data)


# salesordershortbycompanyid
@api_view(['GET'])


def getsalesordershortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": SO.objects.filter(company_id=comp_id,branch_id=branch_id).count()
    }

    # Get the company object by comp_id and apply pagination
    try:

        salesorder = SO.objects.filter(company_id=comp_id,branch_id=branch_id).order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)
    
    
    # Serialize the items and return the paginated response
    response['results'] = SalesOrderShortByCompany_idSerializer(salesorder, many=True).data
    return Response(response)
    

#Sales Order Get Method Section
@api_view(['GET'])


def soDetail(request, pk):
    so = SO.objects.get(id=pk)
    serializer = SOSerializer(so, many=False)
    return Response(serializer.data)


@api_view(['POST'])


def soUpdate(request, pk):
    so = SO.objects.get(id=pk)
    serializer = SOSerializer(instance=so, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# getshortDetails
@api_view(['GET'])


def ShortSalesOrderDetails(request):
    so = SO.objects.all()
    serializer = ShortSalesOrderSerializer(so, many=True)
    return Response(serializer.data)


class SoItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = SO.objects.all()
    serializer_class = JoinSoItemSerializer


    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data
            return Response({
                'data': return_data
            })
        return self.list(request)



#Pagination Section 
@api_view(['GET'])


def getShortPeginatedSalesOrderDetails(request):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": SO.objects.count()}

    queryset = SO.objects.all()[offset:offset + limit]
    serializer = ShortSalesOrderSerializer(queryset, many=True)

    response['results'] = ShortSalesOrderSerializer(queryset, many=True).data
    return Response(response)




#Sales Order update Section
class SalesOrderUpdateViewSet(viewsets.ModelViewSet):
    queryset = SO.objects.all()
    serializer_class =  SalesOrderSerializerUpdate

    
    @transaction.atomic
    def update(self, request, pk, *args, **kwargs):
        so_file_data = None
        try:
            so_data = request.data['data']
            so_data = json.loads(so_data)
            so_file_data = request.FILES.get('attach_file')
        except:
            so_data=request.data
        so= SO.objects.select_for_update().get(so_id=pk)
        so_item_list=[]
        for so_item_data in so_data['so_items']:
            so_item_list.append(so_item_data['item_id'])
           # Item are find Out Section
            print(so_item_data['item_name'])
            try:
                try:
                    so_item = SoItem.objects.select_for_update().get(item_id=so_item_data['item_id'],so_id=so.so_id)
                    
                except KeyError:
                    so_item=None
                    
                  
                                
            except SoItem.DoesNotExist:
                so_item=None
            
            # Invoice Item Are Find the update this Code Section   
            if so_item is not None:
                item_serializer=SOITEMSerializerUpdate(so_item,data=so_item_data)
                if item_serializer.is_valid():
                    item_serializer.save()
                   
            else:
                try:
                    
                   
                    item=Item.objects.get(item_id=so_item_data["item_id"])
                except KeyError:
                   
                    item=None
                
                try:
                    #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
                    new_estimate = SoItem.objects.create(so_id=so,
                                                        item_id=Item.objects.get(item_id=so_item_data["item_id"]),
                                                        item_name=so_item_data["item_name"],
                                                        rate=so_item_data["rate"],
                                                        quantity=so_item_data["quantity"],
                                                        # tax=estimate_items[i]["tax"],
                                                        tax_rate=so_item_data["tax_rate"],
                                                        tax_name=so_item_data["tax_name"],
                                                        tax_type=so_item_data["tax_type"],
                                                        taxamount=so_item_data["taxamount"],
                                                        cgst_amount=so_item_data['cgst_amount'],
                                                        sgst_amount=so_item_data['sgst_amount'],
                                                        igst_amount=so_item_data['igst_amount'],
                                                        amount=so_item_data["amount"])
                    new_estimate.save()
            
                   
                except KeyError:
                    pass                 
                
                    
        print('Not deleted invoice item',so_item_list)        
        del_item = SoItem.objects.filter(so_id=so.so_id).exclude(item_id__in=so_item_list).delete()  
        print("DELETED ITEMS",del_item)
        #this Section Is Invoice Data Update Serializer Through
        serializer = SalesOrderSerializerUpdate(so, data=so_data)

        if serializer.is_valid():
            so_id=serializer.save()
            if so_file_data:
                so.attach_file = so_file_data
        else:

            return Response(serializer.errors, status=400)
           
        return Response(serializer.data)       



# Get SO   by Sales Order Number
@api_view(['GET'])


def getSODetailsBySoNumber(request, so_serial,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    sos = SO.objects.filter(company_id=company_id,so_serial__icontains=so_serial,branch_id=branch_id)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": sos.count()}
    
    instance = sos[offset:offset + limit]
    serializer = SOSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)



#getitemshortbycompanyid
@api_view(['GET'])


def getSOshortbyCustomer_name(request,customer_name,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    sos = SO.objects.filter(company_id=company_id,
                            customer_id__customer_name__icontains=customer_name,branch_id=branch_id)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": sos.count()}
    
    instance = sos[offset:offset + limit]
    

    serializer = SOSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)