
from rest_framework.response import Response
from rest_framework import views, viewsets
from salescustomer.models_old import PR, SO, Invoice, SalesCustomer, SoItem,DC,DcItem,Estimate,EstimatedItem
from .serializers import (DCItemSerializer, EstimatedItemSerializer, SOUpdateSerializer,SOItemSerializer,JoinSoItemSerializer,UpdtJoinSoItemSerializer,
                        DCSerializer,JoinDcItemSerializer,UpdtDcItemSerializer,UpDtEstimateSerializer,
                        EstimateSerializerUpdate,JoinEstimateItemSerializer,EstItemSerializer, updtPRMSerializer,
                        SalesCustomerSerializer,EstimateItemSerializer,EstimatedITEMSerializerUpdate,SalesOrderSerializerUpdate,SOITEMSerializerUpdate,
                        DeliveryChalanSerializerUpdate,DCITEMSerializerUpdate)
from company.models import Company
from item.models import Item
from rest_framework.decorators import api_view, action
from transaction.models import MasterTransaction

from salescustomer import serializers
                    
################### ESTIMATE UPDATE VIEWSETS ######################################


class ShubhamEstimateUpdateViewSet(viewsets.ModelViewSet):
    queryset = Estimate.objects.all()
    serializer_class =  EstimateSerializerUpdate
    def update(self, request, pk, *args, **kwargs):
        #dxfxfddfc
        estimate_data=request.data
        estimate= Estimate.objects.get(est_id=pk)
        comp_id = Company.objects.get(company_id=estimate_data["company_id"])
        cust_id = SalesCustomer.objects.get(
            customer_id=estimate_data["customer_id"])
        
       
        # Invoice Item Looping
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
        serializer = EstimateSerializerUpdate(estimate, data=estimate_data)

        if serializer.is_valid():
            estimate_id=serializer.save()
            
            # return Response({"data":serializer.data})
        else:
            return Response(serializer.errors, status=400)
           
        return Response(serializer.data)


#####################################################
class UpdtPaymentRCvViewset(viewsets.ModelViewSet):
    queryset = PR.objects.all()
    serializer_class=updtPRMSerializer


    def update(self, request, pk, *args, **kwargs):
        pr_data = request.data

        pr = PR.objects.get(pr_id=pk)
        customer_id=SalesCustomer.objects.get(customer_id=pr_data["customer_id"])
        invoice_id=Invoice.objects.get(invoice_id=pr_data['invoice_id'])
        company_id=Company.objects.get(company_id=pr_data['company_id'])


        serializer = updtPRMSerializer(pr, data=pr_data)

        if serializer.is_valid():
            serializer.save()
            msg="Details Updated Successfully"
            
        else:
                return Response(serializer.errors, status=400)    

        account_list=MasterTransaction.objects.get(L1detail_id=pr.pr_id)
        account_list.credit=float(pr_data['amount_received'])
        account_list.debit=float(pr_data['amount_received'])
        account_list.save()

        return Response(serializer.data)    

############################### customer update ##############33
class CustomerUpdtViewset(viewsets.ModelViewSet):
    queryset=SalesCustomer.objects.all()
    serializer_class=SalesCustomerSerializer


    def update(self, request, pk, *args, **kwargs):
        customer_data=request.data     

        try:
            cust= SalesCustomer.objects.get(customer_id=pk)
        except SalesCustomer.DoesNotExist:
            pass

        cust_serializers = SalesCustomerSerializer(cust, data=customer_data)

        if cust_serializers.is_valid():
                cust_serializers.save()
                msg="Details Updated Successfully" 
                return Response(cust_serializers.data)          
        else:
                return Response(cust_serializers.errors, status=400)     


#### sales order update viewset #############
class SalesOrderUpdateViewSet(viewsets.ModelViewSet):
    queryset = SO.objects.all()
    serializer_class =  SalesOrderSerializerUpdate
    def update(self, request, pk, *args, **kwargs):
        #dxfxfddfc
        so_data=request.data
        so= SO.objects.get(so_id=pk)
        comp_id = Company.objects.get(company_id=so_data["company_id"])
        cust_id = SalesCustomer.objects.get(
            customer_id=so_data["customer_id"])
        
       
        # Invoice Item Looping
        so_item_list=[]
        for so_item_data in so_data['so_items']:
            so_item_list.append(so_item_data['item_id'])
           # Item are find Out Section
            print(so_item_data['item_name'])
            try:
                try:
                    so_item = SoItem.objects.get(item_id=so_item_data['item_id'],so_id=so.so_id)
                    
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
            
            # return Response({"data":serializer.data})
        else:
            return Response(serializer.errors, status=400)
           
        return Response(serializer.data)       


@api_view(['GET'])
def getestimateitembyest_id(request, est_id):
    object = EstimatedItem.objects.filter(est_id=est_id)
    serializer = EstItemSerializer(object, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def getest_byestid(request, est_id):
    object = Estimate.objects.filter(est_id=est_id)
    serializer = EstimateSerializerUpdate(object, many=True)
    return Response(serializer.data)


################# DELIVERY CHALLAN UPDATE VIEWSET ##########################3
class DeliveryChalanUpdateViewSet(viewsets.ModelViewSet):
    queryset = DC.objects.all()
    serializer_class =  DeliveryChalanSerializerUpdate
    def update(self, request, pk, *args, **kwargs):
        #dxfxfddfc
        dc_data=request.data
        dc= DC.objects.get(dc_id=pk)
        comp_id = Company.objects.get(company_id=dc_data["company_id"])
        cust_id = SalesCustomer.objects.get(
            customer_id=dc_data["customer_id"])
        
       
        # Invoice Item Looping
        dc_item_list=[]
        for dc_item_data in dc_data['dc_items']:
            dc_item_list.append(dc_item_data['item_id'])
           # Item are find Out Section
            print(dc_item_data['item_name'])
            try:
                try:
                    dc_item = DcItem.objects.get(item_id=dc_item_data['item_id'],dc_id=dc.dc_id)
                    
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
            
            # return Response({"data":serializer.data})
        else:
            return Response(serializer.errors, status=400)
           
        return Response(serializer.data)