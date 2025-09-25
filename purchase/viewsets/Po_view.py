import json
import os
import pandas as pd
import datetime
from pathlib import Path
from wsgiref.util import FileWrapper

from django.template.loader import get_template
from django.views.generic import View
from django.http import HttpResponse, FileResponse
from purchase.printing.generate_po import generate_po_pdf
from utility import save_attach_file
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import api_view

from company.models import Company,Branch,Company_Year
from purchase.models.Po_model import PO
from purchase.models.PoItem_model import PoItem
from purchase.models.Vendor_model import Vendor
from coa.models import COA
from salescustomer.models.Tcs_model import TCS
from purchase.serializers.Po_serializers import POSerializer,purchaseordershortbycompanySerializer,JoinPoItemSerializer,UpdatePOSerializer
from purchase.serializers.Poitem_serializers import PoItemSerializer,UpdtPOItemSerializer
from utility import render_to_pdf
from company.serializers import CompanySerializer
from item.models.item_model import Item
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes

from django.db import transaction
from registration.models import Feature
#Creating the Purchase 

class purchaseorderitemsViewSet(viewsets.ModelViewSet):
    queryset = PoItem.objects.all()
    serializer_class = PoItemSerializer


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        count = Feature.objects.get(user_id=request.user.id).po_remaining
        print(count, 'purchase orders')
        if count <= 0:
            return Response({"message": "You dont have access to this service please upgrade plan"}, status=401)

        po_data_converte = request.data['data']

        print("#################################################")
        print(po_data_converte)
        print("Purchase order Data Format is ", type(po_data_converte))
        print("#################################################")
        # Purchase Convert Str to Dict Code
        po_data = json.loads(po_data_converte)
        print("Converted Format is", type(po_data))

        po_file_data = request.FILES.get('attach_file')
        print("purchaseorder_data", type(po_file_data))

        # cust_id=po_data["customer_id"]
        # if cust_id is not None:
        #     cust_id=SalesCustomer.objects.get(customer_id=cust_id)

        Branch_id = po_data["branch_id"]
        branch_id = Branch.objects.get(branch_id=Branch_id)

        vn_id = po_data["vendor_id"]
        if vn_id is not None:
            vn_id = Vendor.objects.get(vendor_id=vn_id)

        
        company_year_id=po_data.get("company_year_id")
        if company_year_id is not None:
            company_year_id=Company_Year.objects.get(company_year_id=company_year_id)
        
        try:    
            tcs_id = po_data["tcs_id"]
            if tcs_id is not None:
                tcs_id = TCS.objects.get(tcs_id=tcs_id)
        except KeyError:
            tcs_id=None

        po_items = po_data["po_items"]
        comp_id = Company.objects.get(company_id=po_data["company_id"])
        #branch_id = Branch.objects.get(branch_id=estimate_data["branch_id"])
        #cust_id = Customer.objects.get(customer_id=po_data["customer_id"])

        # Purchaseorder Fields
        po_serializer = UpdatePOSerializer(data=po_data)
        if po_serializer.is_valid():
            po_id = po_serializer.save()
            po_id.attach_file = po_file_data
            po_id.save()
        else:
            print(po_serializer.errors)
            return Response(po_serializer.errors,400)

        if po_id. is_converted == True:
            print("*********************",po_id. is_converted)
        
          #  Assign the relevant fields from the estimate object to the sales order object:            
            po_id.From_convt_id=po_data['convt_id']
            po_id.From_convt_ref_no=po_data['convt_ref_no']
            po_id.From_convt_serial=po_data['convt_serial']
            po_id.From_is_converted=po_data["is_converted"]
            print("////////////////////////////////////////",po_id.From_is_converted)
            po_id.From_convt_type=po_data['convt_type']
            po_id.save() 
        
            print("OHHHHHHHHHHHHHHHHH")
            
            
            print("OHHHHHHHHHHHHHHHHH")
            
           # salesorder_id.save()   
            #get estimate by converted id 
            sales_o= Invoice.objects.get(inv_id=po_data['convt_id'])
            print("sales order Object is Here ",po_data.From_convt_id)
            if sales_o.To_is_converted==False:
                sales_o.To_convt_id=po_data.From_convt_id
                sales_o.To_convt_ref_no=po_data.From_convt_ref_no
                sales_o.To_convt_serial=po_data.From_convt_serial
                sales_o.To_is_converted=po_data.From_is_converted
                sales_o.To_convt_type=po_data.From_convt_type
                sales_o.save()
            else:
                return Response("This Estimate Already Converted")
        
        
        

        print("po_created", po_id, type(po_id))

        for i in range(len(po_items)):
            purchase_items = PoItem.objects.create(po_id=po_id,
                                                   item_id=Item.objects.get(
                                                       item_id=po_items[i]["item_id"]),
                                                   coa_id=COA.objects.get(
                                                       coa_id=po_items[i]["coa_id"]),
                                                   # customer_id=SalesCustomer.objects.get(customer_id=po_items[i]["customer_id"]),
                                                   item_name=po_items[i]["item_name"],
                                                   rate=po_items[i]["rate"],
                                                   quantity=po_items[i]["quantity"],
                                                   tax_rate=po_items[i]["tax_rate"],
                                                   tax_name=po_items[i]["tax_name"],
                                                   tax_type=po_items[i]["tax_type"],
                                                   taxamount=po_items[i]["taxamount"],
                                                   discount=po_items[i]["discount"],
                                                   sgst_amount=po_items[i]["sgst_amount"],
                                                   igst_amount=po_items[i]["igst_amount"],
                                                   cgst_amount=po_items[i]["cgst_amount"],
                                                   amount=po_items[i]["amount"])
            purchase_items.save()
            print("purchase_items", purchase_items, type(purchase_items))
        serializer = PoItemSerializer(po_id)  # browser
        return Response(serializer.data)


##################################################
# Dwonload Code Is Creting api By Download
# Download Purchase Order by id

class POFileDownloadListAPIView(generics.ListAPIView):

    def get(self, request, purchaseorder_id, format=None):
        queryset = PO.objects.get(po_id=purchaseorder_id)
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


class POGeneratePdf(View):
    def get(self, request, purchaseoreder_id, *args, **kwargs):
        purchaseorder = PO.objects.get(po_id=purchaseoreder_id)
        # Get The Purchase Order By purchaseoreder_id
        # and Then Serialize the data
        serializer = POSerializer(purchaseorder)
        print(serializer.data)
        # get the Company data In Purchaser Oreder (company_id) related
        print(purchaseorder.company_id.company_id)
        company = Company.objects.get(
            company_id=purchaseorder.company_id.company_id)
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

#Download the Purchase Order
class PODownloadPdf(View):
    def get(self, request, *args, **kwargs):

        # getting the template
        pdf_path = render_to_pdf('invoice.html')

        filename = "po_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)

        # rendering the template

        with open(pdf_path, 'r') as f:
            file_data = f.read()

        # sending response
        response = FileResponse(file_data, as_attachment=True,
                                filename='hello.pdf', content_type='application/pdf')
        response['Content-Disposition'] = content
        return response


##########################################################################################################
#Purchase Order Model view Set Section
class poViewSet(viewsets.ModelViewSet):
    queryset = PO.objects.all()
    serializer_class = POSerializer



#Purchase Order List Api view
class poList(generics.ListAPIView):
    queryset = PO.objects.all()
    serializer_class = POSerializer

    # @api_view Allow to define function that match http methods
    @api_view(['GET'])
    def poCreation(request):
        po = PO.objects.all()
        serializer = POSerializer(po, many=True)
        return Response(serializer.data)


#Get the Comapny id through purchase Order
@api_view(['GET'])
#
def getpurchaseordershortbycompanyid(request, comp_id,branch_id):
    
    # Get the 'limit' and 'offset' parameters from the query string
    limit = int(request.GET.get('limit', 10))  # Default limit is 10 if not provided
    offset = int(request.GET.get('offset', 0))  # Default offset is 0 if not provided

    # Build the response links for pagination
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {
        'next': url + f"?limit={limit}&offset={offset + limit}",
        'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
        "count": PO.objects.filter(company_id=comp_id,branch_id=branch_id).count()
    }

    # Get the company object by comp_id and apply pagination
    try:

        items = PO.objects.filter(company_id=comp_id,branch_id=branch_id).order_by('-created_date')[offset:offset + limit]
    except Company.DoesNotExist:
        return Response("Company not found.", status=404)

    # Serialize the items and return the paginated response
    response['results'] = purchaseordershortbycompanySerializer(items, many=True).data
    return Response(response)
    
    


# api for get bill by company id and bill id
@api_view(['GET'])

def download_po_data(request,po_id):

    # here filter the object of bill id and company id
    purchaseo = PO.objects.select_related('vendor_id','company_id').get(
        po_id=po_id)
    serializers = JoinPoItemSerializer(purchaseo)

    html = generate_po_pdf(data=serializers.data)
    return html

def download_po(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'),as_attachment=True)
    #response = FileResponse(file_data, as_attachment=True,                              
    return response
################################################################################

#Purchase Item Model View
class poitemViewSet(viewsets.ModelViewSet):
    queryset = PoItem.objects.all()
    serializer_class = PoItemSerializer


#Purchase item List Api view
class poitemList(generics.ListAPIView):
    queryset = PoItem.objects.all()
    serializer_class = PoItemSerializer

    # @api_view Allow to define function that match http methods
    @api_view(['GET'])
    def poitemCreation(request):
        poitem = PoItem.objects.all()
        serializer = PoItemSerializer(poitem, many=True)
        return Response(serializer.data)

# Poitem and PO join


class PoItemGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = PO.objects.all()
    serializer_class = JoinPoItemSerializer

    def get(self, request, pk=None):
        if pk:
            return_data = self.retrieve(request, pk).data

            return Response({
                'data': return_data
            })
        return self.list(request)









#Purchase Item Update Section
class PurchaseOrderUpdateViewSet(viewsets.ModelViewSet):
    queryset = PO.objects.all()
    serializer_class =  UpdatePOSerializer
    @transaction.atomic
    def update(self, request, pk, *args, **kwargs):
        po_file_data = None
        try:
            po_data = request.data['data']
            po_data = json.loads(po_data)
            po_file_data = request.FILES.get('attach_file')
        except:
            po_data=request.data
        po= PO.objects.select_for_update().get(po_id=pk)
        po_item_list=[]
        for po_item_data in po_data['po_items']:
            po_item_list.append(po_item_data['item_id'])
           # Item are find Out Section
            print(po_item_data['item_name'])
            try:
                try:
                    po_item = PoItem.objects.select_for_update().get(item_id=po_item_data['item_id'],po_id=po.po_id)
                    
                except KeyError:
                    po_item=None
                    
                  
                                
            except PoItem.DoesNotExist:
                po_item=None
            
            # Invoice Item Are Find the update this Code Section   
            if po_item is not None:
                item_serializer=UpdtPOItemSerializer(po_item,data=po_item_data)
                if item_serializer.is_valid():
                    item_serializer.save()
                   
            else:
                try:
                    
                   
                    item=Item.objects.get(item_id=po_item_data["item_id"])
                except KeyError:
                   
                    item=None
                
                try:
                    #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
                    new_item = PoItem.objects.create(po_id=po,
                                                        item_id=Item.objects.get(item_id=po_item_data["item_id"]),
                                                        item_name=po_item_data["item_name"],
                                                        rate=po_item_data["rate"],
                                                        quantity=po_item_data["quantity"],
                                                        # tax=estimate_items[i]["tax"],
                                                        tax_rate=po_item_data["tax_rate"],
                                                        tax_name=po_item_data["tax_name"],
                                                        tax_type=po_item_data["tax_type"],
                                                        taxamount=po_item_data["taxamount"],
                                                        cgst_amount=po_item_data['cgst_amount'],
                                                        sgst_amount=po_item_data['sgst_amount'],
                                                        igst_amount=po_item_data['igst_amount'],
                                                        amount=po_item_data["amount"])
                    new_item.save()
            
                   
                except KeyError:
                    pass                 
                
                    
        print('Not deleted invoice item',po_item_list)        
        del_item = PoItem.objects.filter(po_id=po.po_id).exclude(item_id__in=po_item_list).delete()  
        print("DELETED ITEMS",del_item)
        #this Section Is Invoice Data Update Serializer Through
        serializer = UpdatePOSerializer(po, data=po_data)
        serializer = UpdatePOSerializer(po, data=po_data)

        if serializer.is_valid():
            so_id=serializer.save()
            if po_file_data:
                po.attach_file = po_file_data
            
            # return Response({"data":serializer.data})
        else:
            return Response(serializer.errors, status=400)
           
        return Response(serializer.data)       

      


# Get search details by po serial number
@api_view(['GET'])

def getPODetailsByPo_serial(request, po_serial,company_id,branch_id):
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    pos = PO.objects.filter(company_id=company_id,
                            branch_id=branch_id,
                            po_serial__icontains=po_serial)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": pos.count()}
    
    instance = pos[offset:offset + limit]
    serializer = POSerializer(instance, many=True)
    
    response['results'] = serializer.data
    return Response(response)


@api_view(['GET'])

def getPODetailsByvendor_name(request,  company_id,vendor_name,branch_id):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    pos = PO.objects.filter(company_id=company_id,
                            branch_id=branch_id,
                            vendor_id__vendor_name__icontains=vendor_name)
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": pos.count()}

    instance = pos[offset:offset + limit]
    serializer = POSerializer(instance, many=True)

    response['results'] = serializer.data
    return Response(response)




#get Purchase order by vendor name
@api_view(['GET'])
#
def getPOshortbyVendor_name(request,vendor_name):   
    
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    
    url = str(request.build_absolute_uri()).split("?")[0]
    response = {'next': url + f"?limit={limit}&offset={offset + limit}",
                'previous': url + f"?limit={limit}&offset={offset - limit}" if offset > 0 else None,
                "count": Vendor.objects.count()}
    
    instance = Vendor.objects.filter(vendor_name__icontains=vendor_name)[offset:offset + limit]
    
    serializer = VendorSer(instance, many=True)
   # return Response(serializer.data)

    if serializer.data:
        customer_id = serializer.data[0].get('customer_id')
        print("Estimate data is **********************", customer_id)
        coa = CreditNote.objects.filter(customer_id=customer_id)
    else:
        # Handle the case where there are no instances in the list
        coa = None  # You may want to handle this differently based on your use case
    serializer = CreditNoteSerializer(coa, many=True)
    
    response['results'] = CreditNoteSerializer(coa, many=True).data
    return Response(response)
