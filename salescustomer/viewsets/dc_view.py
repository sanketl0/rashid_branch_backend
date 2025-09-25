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
from salescustomer.printing.generate_dc import generate_dc_pdf
from utility import render_to_pdf
from re import template
from xhtml2pdf import pisa
from rest_framework import status
from salescustomer.models.Dc_item_model import DcItem
from salescustomer.serializers.Dc_item_serializers import DcItemSerializer,DCITEMSerializerUpdate
from salescustomer.models.Dc_model import DC
from salescustomer.serializers.Dc_serializers import DCSerializer,JoinDcItemSerializer,ShortDeliveryChallanSerializer,dcshortbycompanySerializer,DeliveryChalanSerializerUpdate
from salescustomer.models.Salescustomer_model import SalesCustomer
from salescustomer.models.Tcs_model import TCS
from item.models.item_model import Item
from item.models.stock_model import Stock
from company.serializers import CompanySerializer
from utility import save_attach_file
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from coa.models import COA
from salescustomer.models.So_model import SO
from salescustomer.serializers.Salescustomer_serializers import SalesCustomerSerializer
from django.db import transaction
from registration.models import Feature
class dcitemsViewSet(viewsets.ModelViewSet):
    queryset = DcItem.objects.all()
    serializer_class = DcItemSerializer

    

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        count = Feature.objects.get(user_id=request.user.id).dc_remaining
        print(count, 'delivery challan')
        if count <= 0:
            return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)

        dc_data_converte = request.data['data']
        print("#################################################")
        print(dc_data_converte)
        print("Delivary Challan Data Format is ", type(dc_data_converte))
        print("#################################################")
        # Delivary Challan Convert Str to Dict Code
        dc_data = json.loads(dc_data_converte)
        print("Converted Format is", type(dc_data))

        dc_file_data = request.FILES.get('attach_file')
        print("dc_data", type(dc_file_data))

        

        try:    
            tcs_id = dc_data["tcs_id"]
            if tcs_id is not None:
                tcs_id = TCS.objects.get(tcs_id=tcs_id)
        except KeyError:
            tcs_id=None
        dc_items = dc_data["dc_items"]
        comp_id = Company.objects.get(company_id=dc_data["company_id"])
        branch_id = Branch.objects.get(branch_id=dc_data["branch_id"])
        cust_id = SalesCustomer.objects.get(customer_id=dc_data["customer_id"])

        # Delivery Challan fields
        deliverychallan_id = DC.objects.create(dc_ref_no=dc_data["dc_ref_no"],
                                               dc_date=dc_data["dc_date"],
                                               dc_status=dc_data["dc_status"],
                                               dc_serial=dc_data["dc_serial"],
                                               is_dc_generated=dc_data["is_dc_generated"],
                                               customer_note=dc_data["customer_note"],
                                               discount=dc_data["discount"],
                                               entered_discount=dc_data["entered_discount"],
                                               entered_shipping_charges=dc_data["entered_shipping_charges"],
                                               shipping_charges=dc_data["shipping_charges"],
                                               shipping_tax_name=dc_data["shipping_tax_name"],
                                               shipping_tax_rate=dc_data["shipping_tax_rate"],
                                               dc_type=dc_data["dc_type"],
                                               supply_place=dc_data["supply_place"],
                                               terms_condition=dc_data["terms_condition"],
                                               total_gst=dc_data["total_gst"],
                                               cgst_total=dc_data['cgst_total'],
                                               sgst_total=dc_data['sgst_total'],
                                               igst_total=dc_data['igst_total'],
                                               # expiry_date=dc_data["expiry_date"],
                                               # tcs_amount=dc_data["tcs_amount"],
                                               sub_total=dc_data["sub_total"],
                                               total=dc_data["total"],
                                               tcs_id=tcs_id,
                                               # payment_id = pay_id,
                                               # emp_id = employee_id,
                                               company_id=comp_id,
                                               branch_id=branch_id,
                                               attach_file=dc_file_data,
                                               is_converted=dc_data['is_converted'],
                                               customer_id=cust_id)

        deliverychallan_id.save()
        print("************************** CODE IS EXECUTING HERE************")
        if deliverychallan_id. is_converted == True:
            print("*********************",deliverychallan_id. is_converted)
        
          #  Assign the relevant fields from the estimate object to the sales order object:            
            deliverychallan_id.From_convt_id=dc_data['convt_id']
            deliverychallan_id.From_convt_ref_no=dc_data['convt_ref_no']
            deliverychallan_id.From_convt_serial=dc_data['convt_serial']
            deliverychallan_id.From_is_converted=dc_data["is_converted"]
            print("////////////////////////////////////////")
            deliverychallan_id.From_convt_type=dc_data['convt_type']
            deliverychallan_id.save() 
        
            print("OHHHHHHHHHHHHHHHHH")
            
            
            print("OHHHHHHHHHHHHHHHHH")
            
           # salesorder_id.save()   
            #get estimate by converted id 
            est= SO.objects.get(so_id=dc_data['convt_id'])
            print("sales order Object is Here ",deliverychallan_id.From_convt_id)
            if est.To_is_converted==False:
                est.To_convt_id=deliverychallan_id.From_convt_id
                est.To_convt_ref_no=deliverychallan_id.From_convt_ref_no
                est.To_convt_serial=deliverychallan_id.From_convt_serial
                est.To_is_converted=deliverychallan_id.From_is_converted
                est.To_convt_type=deliverychallan_id.From_convt_type
                est.save()
            # else:
            #     return Response({"message":"This Estimate Already Converted"},status=400)

        print("so_items", dc_items, type(dc_items))

        for i in range(len(dc_items)):
            new_dcitem = DcItem.objects.create(dc_id=deliverychallan_id,
                                               item_id=Item.objects.get(
                                                   item_id=dc_items[i]["item_id"]),
                                               item_name=dc_items[i]["item_name"],
                                               rate=dc_items[i]["rate"],
                                               quantity=dc_items[i]["quantity"],
                                               tax_rate=dc_items[i]["tax_rate"],
                                               tax_name=dc_items[i]["tax_name"],
                                               tax_type=dc_items[i]["tax_type"],
                                               taxamount=dc_items[i]["taxamount"],
                                               cgst_amount=dc_items[i]['cgst_amount'],
                                               sgst_amount=dc_items[i]['sgst_amount'],
                                               igst_amount=dc_items[i]['igst_amount'],
                                               amount=dc_items[i]["amount"],
                                               coa_id=COA.objects.get(
                                                   coa_id=dc_items[i]["coa_id"]))

            new_dcitem.save()
            print(i, "dc_items")

            # serializer = DcItemSerializer(new_dcitem)  # browser
        return Response(status=status.HTTP_201_CREATED)


##################################################
# Dwonload Code Is Creting api By Download
# Download Delivary Challan by id

class DelivarychallanFileDownloadListAPIView(generics.ListAPIView):

    def get(self, request, dc_id, format=None):
        queryset = DC.objects.get(dc_id=dc_id)
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

#Delivary Challen Generate Pdf
class DelivaryChallenGeneratePdf(View):
    def get(self, request, dc_id, *args, **kwargs):
        dc = DC.objects.get(dc_id=dc_id)
        # Get The Estimate By estimate id
        # and Then Serialize the data
        serializer = DCSerializer(dc)
        print(serializer.data)
        # get the Company data In Estimate (company_id) related
        print(dc.company_id.company_id)
        company = Company.objects.get(company_id=dc.company_id.company_id)
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
#Delivary Challen DwonloadPdf
class DelivarychallenDownloadPdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        pdf_path = render_to_pdf('invoice.html')

        filename = "delivary_%s.pdf" % ("12341231")
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
#Delivary Challen Id wise Data geting 

@api_view(['GET'])


def dcDetail(request, pk):
    dc = DC.objects.get(id=pk)
    serializer = DCSerializer(dc, many=False)
    return Response(serializer.data)

#fUNCTION BASED pOST 
@api_view(['POST'])


def dcUpdate(request, pk):
    dc = DC.objects.get(id=pk)
    serializer = DCSerializer(instance=dc, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# getshortDetails
@api_view(['GET'])


def ShortDeliveryChallanDetails(request):
    dc = DC.objects.all()
    serializer = ShortDeliveryChallanSerializer(dc, many=True)
    return Response(serializer.data)


# dcshortbycompanyid
@api_view(['GET'])


def dcshortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided
    
    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": DC.objects.filter(company_id=comp_id,branch_id=branch_id).count()
    }

    # Get the company object by comp_id and apply pagination
    try:

        dc = DC.objects.filter(company_id=comp_id,branch_id=branch_id).order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = dcshortbycompanySerializer(dc, many=True).data
    return Response(response)
    


#############################################################
###############################################################3##########################



# api for get bill by company id and bill id
@api_view(['GET'])

   
def download_dc_data(request,dc_id):

    dc = DC.objects.get(dc_id=dc_id)
    # here filter the object of bill id and company id
    serializers =JoinDcItemSerializer(dc)

    html = generate_dc_pdf(data=serializers.data)
    
    return html

def download_dc(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'),as_attachment=True)
    #response = FileResponse(file_data, as_attachment=True,                              
    return response
################################################################################

# Dcitem and DC join
class DcItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = DC.objects.all()
    serializer_class = JoinDcItemSerializer

    #
    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data
            return Response({
                'data': return_data
            })
        return self.list(request)






################# DELIVERY CHALLAN UPDATE VIEWSET ##########################3
class DeliveryChalanUpdateViewSet(viewsets.ModelViewSet):
    queryset = DC.objects.all()
    serializer_class =  DeliveryChalanSerializerUpdate

    

    @transaction.atomic
    def update(self, request, pk, *args, **kwargs):
        dc_file_data = None
        try:
            dc_data = request.data['data']
            dc_data = json.loads(dc_data)
            dc_file_data = request.FILES.get('attach_file')
        except:
            dc_data=request.data
        dc= DC.objects.select_for_update().get(dc_id=pk)

       
        # Invoice Item Looping
        dc_item_list=[]
        for dc_item_data in dc_data['dc_items']:
            dc_item_list.append(dc_item_data['item_id'])
           # Item are find Out Section
            print(dc_item_data['item_name'])
            try:
                try:
                    dc_item = DcItem.objects.select_for_update().get(item_id=dc_item_data['item_id'],dc_id=dc.dc_id)
                    
                except KeyError:
                    dc_item=None
                    
                  
                                
            except DcItem.DoesNotExist:
                dc_item=None
            
            # Invoice Item Are Find the update this Code Section   
            if dc_item is not None:
                item_serializer=DCITEMSerializerUpdate(dc_item,data=dc_item_data)
                if item_serializer.is_valid():
                    item_serializer.save()
                   
            else:
                try:
                    
                   
                    item=Item.objects.get(item_id=dc_item_data["item_id"])
                except KeyError:
                   
                    item=None
                
                try:
                    #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
                    new_dcitem = DcItem.objects.create(dc_id=dc,
                                                        item_id=Item.objects.get(item_id=dc_item_data["item_id"]),
                                                        item_name=dc_item_data["item_name"],
                                                        rate=dc_item_data["rate"],
                                                        quantity=dc_item_data["quantity"],
                                                        # tax=estimate_items[i]["tax"],
                                                        tax_rate=dc_item_data["tax_rate"],
                                                        tax_name=dc_item_data["tax_name"],
                                                        tax_type=dc_item_data["tax_type"],
                                                        taxamount=dc_item_data["taxamount"],
                                                        cgst_amount=dc_item_data['cgst_amount'],
                                                        sgst_amount=dc_item_data['sgst_amount'],
                                                        igst_amount=dc_item_data['igst_amount'],
                                                        amount=dc_item_data["amount"])
                    new_dcitem.save()
            
                   
                except KeyError:
                    pass                 
                
                    
        print('Not deleted invoice item',dc_item_list)        
        del_item = DcItem.objects.filter(dc_id=dc.dc_id).exclude(item_id__in=dc_item_list).delete()  
        print(' deleted  item',del_item)  
        #this Section Is Invoice Data Update Serializer Through
        serializer = DeliveryChalanSerializerUpdate(dc, data=dc_data)

        if serializer.is_valid():
            dc_id=serializer.save()
            if dc_file_data:
                dc.attach_file = dc_file_data
            # return Response({"data":serializer.data})
        else:
            return Response(serializer.errors, status=400)
           
        return Response(serializer.data)
    
    
    
#Delivary Challen Pagination Details
@api_view(['GET'])


def getShortPeginatedDeliveryChallanDetails(request):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": DC.objects.count()}

    queryset = DC.objects.all()[offset:offset + limit]
    serializer = ShortDeliveryChallanSerializer(queryset, many=True)

    response['results'] = ShortDeliveryChallanSerializer(queryset, many=True).data
    return Response(response)



# Get Delivery Chalan details by Delivery Chalan  Number 
@api_view(['GET'])


def getDCDetailsByDC_Serial(request, dc_serial,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    dcs = DC.objects.filter(company_id=company_id,dc_serial__icontains=dc_serial,branch_id=branch_id)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": dcs.count()}
    
    instance = dcs[offset:offset + limit]
    serializer = DCSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)




@api_view(['GET'])

#
def getDCshortbyCustomer_name(request,customer_name,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    dcs =  DC.objects.filter(company_id=company_id,customer_id__customer_name__icontains=customer_name,branch_id=branch_id)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count":dcs.count()}
    
    instance = dcs[offset:offset + limit]

    serializer = DCSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)