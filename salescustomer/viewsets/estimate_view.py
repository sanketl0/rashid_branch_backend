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
from salescustomer.printing.generate_est import generate_estimate_pdf
from utility import render_to_pdf
from company.serializers import CompanySerializer
from salescustomer.models.Estimated_item_model import EstimatedItem
from salescustomer.models.Estimate_model import Estimate
from salescustomer.serializers.Estimate_serializers import EstimateSerializerUpdateGet, EstimateNewSerializer, EstimateSerializer,JoinEstimateItemSerializer,ShortEstimateSerializer,JoinItemSerializer,EstimateSerializerUpdate,GetestimateShortbycompany_idEstimateSerializer,PropertyDetailSerializer
from salescustomer.serializers.Estimated_item_serializers import EstimatedItemSerializer,EstimatedITEMSerializerUpdate
from salescustomer.models.Employee_model import Employee
from salescustomer.models.Tcs_model import TCS 
from salescustomer.models.Salescustomer_model import SalesCustomer
from transaction.models import MasterTransaction
from item.models.item_model import Item
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from utility import save_attach_file
from coa.models import COA
from salescustomer.serializers.Salescustomer_serializers import SalesCustomerSerializer
from rest_framework.parsers import MultiPartParser,JSONParser,FormParser
#Estimated Item Creation Section
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from registration.models import Feature
class EstimatedView(APIView):

    parser_classes =[MultiPartParser]

    def post(self,request):
        print(request.data)
        serializer = EstimateNewSerializer(data=request.data)
        print(serializer.is_valid())
        serializer.save()
        print(serializer.data)
        print(serializer.errors)
        return Response(status=status.HTTP_201_CREATED)




class estimateitemsViewSet(viewsets.ModelViewSet):
    queryset = EstimatedItem.objects.all()
    serializer_class = EstimatedItemSerializer

    parser_classes =[MultiPartParser]
    

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        count = Feature.objects.get(user_id=request.user.id).estimates_remaining
        print(count, 'estimates')
        if count <= 0:
            return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)

        try:
            print(request.data)
            estimate_data_converte = request.data['data']
            estimate_data = json.loads(estimate_data_converte)
        except:
            del request.data['attach_file']
            estimate_data = dict(json.dumps(request.data))

        # PR Convert Str to Dict Code

        estimate_file_data = request.FILES.get('attach_file')
        employee_id = estimate_data["emp_id"]
        if employee_id is not None:
            employee_id = Employee.objects.get(emp_id=employee_id)

        try:    
            tcs_id = estimate_data["tcs_id"]
            if tcs_id is not None:
                tcs_id = TCS.objects.get(tcs_id=tcs_id)
        except KeyError:
            tcs_id=None
        
        Branch_id = estimate_data["branch_id"]
        branch_id = Branch.objects.get(branch_id=Branch_id)


        estimate_items = estimate_data["estimate_items"]
        comp_id = Company.objects.get(company_id=estimate_data["company_id"])
        cust_id = SalesCustomer.objects.get(
            customer_id=estimate_data["customer_id"])

        # Estimate fields
        estimate_id = Estimate.objects.create(est_ref_no=estimate_data["est_ref_no"],
                                              est_date=estimate_data["est_date"],
                                              est_status=estimate_data["est_status"],
                                              est_serial=estimate_data["est_serial"],
                                              # notes=estimate_data["notes"],
                                              # journal_type=estimate_data["journal_type"],
                                              is_estimate_generated=estimate_data["is_estimate_generated"],
                                              # attach_file=estimate_data["attach_file"],
                                              customer_note=estimate_data["customer_note"],
                                              discount=estimate_data["discount"],
                                              entered_discount=estimate_data["entered_discount"],
                                              entered_shipping_charges=estimate_data["entered_shipping_charges"],
                                              shipping_charges=estimate_data["shipping_charges"],
                                              shipping_tax_name=estimate_data["shipping_tax_name"],
                                              shipping_tax_rate=estimate_data["shipping_tax_rate"],
                                              subject=estimate_data["subject"],
                                              supply_place=estimate_data["supply_place"],
                                              terms_condition=estimate_data["terms_condition"],
                                              total_gst=estimate_data["total_gst"],
                                              total_quantity=estimate_data["total_quantity"],
                                              expiry_date=estimate_data["expiry_date"],
                                              tcs_amount=estimate_data["tcs_amount"],
                                              sub_total=estimate_data["sub_total"],
                                              total=estimate_data["total"],
                                              # amount=estimate_data["amount"],
                                              cgst_total=estimate_data['cgst_total'],
                                              sgst_total=estimate_data['sgst_total'],
                                              igst_total=estimate_data['igst_total'],
                                              attach_file=estimate_file_data,
                                              company_id=comp_id,
                                              branch_id=branch_id,
                                              customer_id=cust_id,
                                              tcs_id=tcs_id,
                                              emp_id=employee_id)
        estimate_id.save()

        for i in range(len(estimate_items)):
            print(estimate_items[i]["tax_name"])
            new_estimate = EstimatedItem.objects.create(est_id=estimate_id,
                                                       item_id=Item.objects.get(
                                                            item_id=estimate_items[i]["item_id"]), 
                                                        # customer_id = SalesCustomer.objects.get(customer_id=estimate_items[i]["customer_id"],
                                                        # company_id = comp_id,
                                                        item_name=estimate_items[i]["item_name"],
                                                        rate=estimate_items[i]["rate"],
                                                        quantity=estimate_items[i]["quantity"],
                                                        # tax=estimate_items[i]["tax"],
                                                        tax_rate=estimate_items[i]["tax_rate"],
                                                        tax_name=estimate_items[i]["tax_name"],
                                                        tax_type=estimate_items[i]["tax_type"],
                                                        taxamount=estimate_items[i]["taxamount"],
                                                        cgst_amount=estimate_items[i]['cgst_amount'],
                                                        sgst_amount=estimate_items[i]['sgst_amount'],
                                                        igst_amount=estimate_items[i]['igst_amount'],
                                                        amount=estimate_items[i]["amount"],
                                                        # Here add coa_id field bacause facing error of coa is null while testing the converting
                                                        # addd coa in estimate item model also.
                                                        coa_id=COA.objects.get(
                                                            coa_id=estimate_items[i]["coa_id"]))
            new_estimate.save()
            print(i, "estimate_items")
        serializer = EstimatedItemSerializer(new_estimate)  # browser
        return Response(serializer.data)


##################################################
# Dwonload Code Is Creting api By Download
# Download Estimet by id

class EstimateFileDownloadListAPIView(generics.ListAPIView):

    def get(self, request, estimate_id, format=None):
        queryset = Estimate.objects.get(est_id=estimate_id)
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
            return HttpResponse("No File Found")


#######################################################

#Estimated Genrate Pdf
class EstimateGeneratePdf(View):
    def get(self, request, estimate_id, *args, **kwargs):
        estimate = Estimate.objects.get(est_id=estimate_id)
        # Get The Estimate By estimate id
        # and Then Serialize the data
        serializer = EstimateSerializer(estimate)
        print(serializer.data)
        # get the Company data In Estimate (company_id) related
        print(estimate.company_id.company_id)
        company = Company.objects.get(
            company_id=estimate.company_id.company_id)
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

#Estimate Download section 
class EstimateDownloadPdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        pdf_path = render_to_pdf('invoice.html')

        filename = "estimate_%s.pdf" % ("12341231")
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
###############################################################3##########################

# api for get bill by company id and bill id
@api_view(['GET'])

# 
def download_est_data(request, est_id):

    estimate = Estimate.objects.select_related('customer_id','company_id').get(est_id=est_id)
    serializers =JoinEstimateItemSerializer(estimate)
    # return Response(serializers.data,status=200)
    html = generate_estimate_pdf(data=serializers.data)
    return html


def download_est(request, file_name):
   # file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    file_path = f"media/{file_name}"
  #  print("""""""""""""''---------------------------------------------------------------------",output_path)
    response = FileResponse(open( file_path,'rb'))
  #  return FileResponse(open(output_path, 'rb'), as_attachment=True)

    #response = FileResponse(file_data, as_attachment=True,                              
    return response
################################################################################





# ESTIMATE
class estimateViewSet(viewsets.ModelViewSet):
    queryset = Estimate.objects.all()
    serializer_class = EstimateSerializer

    

class estimateList(generics.ListAPIView):
    queryset = Estimate.objects.order_by('created_date')
    serializer_class = EstimateSerializer

    # @api_view Allow to define function that match http methods
    @api_view(['GET'])
    def estimateCreation(self, request):
        estimate = Estimate.objects.all()
        serializer = EstimateSerializer(estimate, many=True)
        return Response(serializer.data)


# estimateshortbycompanyid
@api_view(['GET'])

#
def getestimateshortbycompanyid(request, comp_id,branch_id):
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": Estimate.objects.filter(company_id=comp_id,branch_id=branch_id).count()
    }
    
    # Get the company object by comp_id and apply pagination
    try:
        estimate = Estimate.objects.filter(company_id=comp_id,branch_id=branch_id).order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)
    
    # Serialize the items and return the paginated response
    response['results'] = EstimateSerializer(estimate, many=True).data
    return Response(response)


# getshortDetails
@api_view(['GET'])


def ShortEstimateDetails(request):
    estimate = Estimate.objects.all()
    serializer = ShortEstimateSerializer(estimate, many=True)
    return Response(serializer.data)

#Est_id wise the Featching the all data 
@api_view(['GET'])


def estimateDetail(request, pk):
    estimate = Estimate.objects.get(est_id=pk)
    serializer = EstimateSerializer(estimate, many=False)
    return Response(serializer.data)

#Function based Simple post
@api_view(['POST'])


def estimateUpdate(request, pk):
    estimate = Estimate.objects.get(est_id=pk)
    serializer = EstimateSerializer(instance=estimate, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# Estimate and Item join
class EstimateGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Estimate.objects.all()
    serializer_class = JoinItemSerializer

    
    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })
        return self.list(request)

    # Estimateditem and Estimate join


class EstimatedItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Estimate.objects.all()
    serializer_class = JoinEstimateItemSerializer

  #  
    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data

            return Response({
                'data': return_data
            })
        return self.list(request)







@api_view(['GET'])


def getPeginatedShortEstimateDetails(request):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": Estimate.objects.count()}

    queryset = Estimate.objects.all()[offset:offset + limit]
    serializer = ShortEstimateSerializer(queryset, many=True)

    response['results'] = ShortEstimateSerializer(queryset, many=True).data
    return Response(response)

#Pagination Section For Estimeted Page 
@api_view(['GET'])


def getAllPeginatedEstimateDetails(request):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": Estimate.objects.count()}

    queryset = Estimate.objects.all()[offset:offset + limit]
    serializer = EstimateSerializer(queryset, many=True)

    response['results'] = EstimateSerializer(queryset, many=True).data
    return Response(response)














class ShubhamEstimateUpdateViewSet(viewsets.ModelViewSet):
    queryset = Estimate.objects.all()
    serializer_class =  EstimateSerializerUpdate

    @transaction.atomic
    def update(self, request, pk, *args, **kwargs):
        estimate_file_data = None
        try:
            estimate_data = request.data['data']
            estimate_data = json.loads(estimate_data)
            estimate_file_data = request.FILES.get('attach_file')
            print(estimate_file_data,"here",type(estimate_file_data))
        except:
            estimate_data = request.data

        estimate= Estimate.objects.select_for_update().get(est_id=pk)
        estimate_item_list=[]
        for estimate_item_data in estimate_data['estimate_items']:
            estimate_item_list.append(estimate_item_data['item_id'])
           # Item are find Out Section
            print(estimate_item_data['item_name'])
            try:
                try:
                    estimate_item = EstimatedItem.objects.get(item_id=estimate_item_data['item_id'],est_id=estimate.est_id)
                    
                except KeyError:
                    estimate_item=None
                    
                  
                                
            except EstimatedItem.DoesNotExist:
                estimate_item=None
            
            # Invoice Item Are Find the update this Code Section   
            if estimate_item is not None:
                item_serializer=EstimatedITEMSerializerUpdate(estimate_item,data=estimate_item_data)
                if item_serializer.is_valid():
                    item_serializer.save()
                   
            else:
                try:
                    
                   
                    item=Item.objects.get(item_id=estimate_item_data["item_id"])
                except KeyError:
                   
                    item=None
                
                try:
                    #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
                    new_estimate = EstimatedItem.objects.create(est_id=estimate,
                                                        item_id=Item.objects.get(item_id=estimate_item_data["item_id"]),
                                                        item_name=estimate_item_data["item_name"],
                                                        rate=estimate_item_data["rate"],
                                                        quantity=estimate_item_data["quantity"],
                                                        # tax=estimate_items[i]["tax"],
                                                        tax_rate=estimate_item_data["tax_rate"],
                                                        tax_name=estimate_item_data["tax_name"],
                                                        tax_type=estimate_item_data["tax_type"],
                                                        taxamount=estimate_item_data["taxamount"],
                                                        cgst_amount=estimate_item_data['cgst_amount'],
                                                        sgst_amount=estimate_item_data['sgst_amount'],
                                                        igst_amount=estimate_item_data['igst_amount'],
                                                        amount=estimate_item_data["amount"])
                    new_estimate.save()
            
                   
                except KeyError:
                    pass                 
                
                    
        print('Not deleted invoice item',estimate_item_list)        
        del_item = EstimatedItem.objects.filter(est_id=estimate.est_id).exclude(item_id__in=estimate_item_list).delete()  
        #this Section Is Invoice Data Update Serializer Through
        serializer = EstimateSerializerUpdateGet(estimate, data=estimate_data)

        if serializer.is_valid():
            serializer.save()
            if estimate_file_data:
                estimate.attach_file = estimate_file_data
                estimate.save()
            # return Response({"data":serializer.data})
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)
           
        return Response(serializer.data)




@api_view(['GET'])


def getest_byestid(request, est_id):
    object = Estimate.objects.filter(est_id=est_id)
    serializer = EstimateSerializerUpdate(object, many=True)
    return Response(serializer.data)



# Get search Estimete  by Estimate Number
@api_view(['GET'])


def getEsatimateDetailsByEstimateNumber(request, est_serial,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": Estimate.objects.filter(company_id=company_id,est_serial__icontains=est_serial,branch_id=branch_id).count()}
    
    instance = Estimate.objects.filter(company_id=company_id,est_serial__icontains=est_serial,branch_id=branch_id)[offset:offset + limit]
    serializer = EstimateSerializer(instance, many=True)
    
    response['results'] = EstimateSerializer(instance, many=True).data
    return Response(response)


import time
#getitemshortbycompanyid
@api_view(['GET'])


def getEstimateshortbyCustomer_name(request,customer_name,company_id,branch_id):
    
    
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": SalesCustomer.objects.filter(company_id=company_id,branch_id=branch_id).count()}
    start_time = time.time()
    coa = Estimate.objects.filter(company_id=company_id,
                                  branch_id=branch_id,
                                  customer_id__customer_name__icontains=customer_name)

    serializer = EstimateSerializer(coa, many=True)
    
    response['results'] = serializer.data
    return Response(response)
    
    
    
   