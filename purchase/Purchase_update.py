# from rest_framework import viewsets
# from rest_framework.response import Response
# from purchase.models import *

# from purchase.serializers import *

# from company.models import Company
# from purchase.serializers import UpdatePOSerializer
# from purchase.models import PaymentMade
# from item.models import Item

# from salescustomer.models import SalesCustomer
# from transaction.models import MasterTransaction
                                              


# ################### EXPENSE ROCORD UPDATE VIEWSETS ############################

# class ExpenseUpdateViewset(viewsets.ModelViewSet):
#     queryset = ExpenseRecord.objects.all()
#     serializer_class=UpdTExpenseRecordSerializer

#     def update(self, request, pk, *args, **kwargs):
#         exps_data = request.data

#         exp_id = ExpenseRecord.objects.get(er_id=pk)
#        # cust_id = SalesCustomer.objects.get(customer_id=exps_data["customer_id"])
#         vn_id=Vendor.objects.get(vendor_id=exps_data["vendor_id"])

#         serializer = UpdTExpenseRecordSerializer(exp_id, data=exps_data)

#         if serializer.is_valid():
#             serializer.save()
#             msg="Details Updated Successfully"
#             return Response({"message":msg,"data":serializer.data,"status":200})
#         else:
#                 return Response(serializer.errors, status=400)

# ################## UPDATE PAYMENT MADE API ###############

# class UpdtPaymentMadeViewset(viewsets.ModelViewSet):
#     queryset = PaymentMade.objects.all()
#     serializer_class=UpdtPaymentmadeSerializer


#     def update(self, request, pk, *args, **kwargs):
#         pm_data = request.data

#         pm = PaymentMade.objects.get(pm_id=pk)
#         vn_id=Vendor.objects.get(vendor_id=pm_data["vendor_id"])
#         print("API IS HEATING HERE")
#         serializer = UpdtPaymentmadeSerializer(pm, data=pm_data)

#         if serializer.is_valid():
#             serializer.save()
#             msg="Details Updated Successfully"           
#         else:
#             return Response(serializer.errors, status=400)

#         account_list=MasterTransaction.objects.get(L1detail_id=pm.pm_id)
#         account_list.credit=float(pm_data['amount_payable'])
#         account_list.debit=float(pm_data['amount_payable'])
#         account_list.save()

#         return Response(serializer.data)



# ################### VENDOR UPDATE VIEWSETS ##############################

# class VendorUpdtViewset(viewsets.ModelViewSet):
#     queryset=Vendor.objects.all()
#     serializer_class=VendorSerializer


#     def update(self, request, pk, *args, **kwargs):
#         vendor_data=request.data
#         print(" REQUEST DATA",vendor_data)
       

#         try:
#             vendor = Vendor.objects.get(vendor_id=pk)
#         except Vendor.DoesNotExist:
#             pass

#         vn_serializers = VendorSerializer(vendor, data=vendor_data)

#         if vn_serializers.is_valid():
#                 vn_serializers.save()
#                 msg="Details Updated Successfully" 
#                 return Response(vn_serializers.data)          
#         else:
#                 return Response(vn_serializers.errors, status=400)


                
        


# ##################################################################

# class PurchaseOrderUpdateViewSet(viewsets.ModelViewSet):
#     queryset = PO.objects.all()
#     serializer_class =  UpdatePOSerializer
#     def update(self, request, pk, *args, **kwargs):
#         #dxfxfddfc
#         po_data=request.data
#         po= PO.objects.get(po_id=pk)
#         comp_id = Company.objects.get(company_id=po_data["company_id"])
#       #  cust_id = SalesCustomer.objects.get(
#           #  customer_id=po_data["customer_id"])
        
       
#         # Invoice Item Looping
#         po_item_list=[]
#         for po_item_data in po_data['po_items']:
#             po_item_list.append(po_item_data['item_id'])
#            # Item are find Out Section
#             print(po_item_data['item_name'])
#             try:
#                 try:
#                     po_item = PoItem.objects.get(item_id=po_item_data['item_id'],po_id=po.po_id)
                    
#                 except KeyError:
#                     po_item=None
                    
                  
                                
#             except PoItem.DoesNotExist:
#                 po_item=None
            
#             # Invoice Item Are Find the update this Code Section   
#             if po_item is not None:
#                 item_serializer=UpdtPOItemSerializer(po_item,data=po_item_data)
#                 if item_serializer.is_valid():
#                     item_serializer.save()
                   
#             else:
#                 try:
                    
                   
#                     item=Item.objects.get(item_id=po_item_data["item_id"])
#                 except KeyError:
                   
#                     item=None
                
#                 try:
#                     #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
#                     new_item = PoItem.objects.create(po_id=po,
#                                                         item_id=Item.objects.get(item_id=po_item_data["item_id"]),
#                                                         item_name=po_item_data["item_name"],
#                                                         rate=po_item_data["rate"],
#                                                         quantity=po_item_data["quantity"],
#                                                         # tax=estimate_items[i]["tax"],
#                                                         tax_rate=po_item_data["tax_rate"],
#                                                         tax_name=po_item_data["tax_name"],
#                                                         tax_type=po_item_data["tax_type"],
#                                                         taxamount=po_item_data["taxamount"],
#                                                         cgst_amount=po_item_data['cgst_amount'],
#                                                         sgst_amount=po_item_data['sgst_amount'],
#                                                         igst_amount=po_item_data['igst_amount'],
#                                                         amount=po_item_data["amount"])
#                     new_item.save()
            
                   
#                 except KeyError:
#                     pass                 
                
                    
#         print('Not deleted invoice item',po_item_list)        
#         del_item = PoItem.objects.filter(po_id=po.po_id).exclude(item_id__in=po_item_list).delete()  
#         print("DELETED ITEMS",del_item)
#         #this Section Is Invoice Data Update Serializer Through
#         serializer = UpdatePOSerializer(po, data=po_data)

#         if serializer.is_valid():
#             so_id=serializer.save()
            
#             # return Response({"data":serializer.data})
#         else:
#             return Response(serializer.errors, status=400)
           
#         return Response(serializer.data)       

      




# @api_view(['GET'])
# def getdebitnoteitembydn_id(request, dn_id):
#     object = DebitItem.objects.filter(dn_id=dn_id)
#     serializer = UpdatesDebitnoteItemSerializer(object, many=True)
#     return Response(serializer.data)        





# class DebitnoteUpdate3ViewSet(viewsets.ModelViewSet):
#     queryset = DebitNote.objects.all()
#     serializer_class = DebitnoteSerializer
#     def update(self, request, pk, *args, **kwargs):
#         debitnote_data=request.data
#         debitnote = DebitNote.objects.get(dn_id=pk)
#         comp_id = Company.objects.get(company_id=debitnote_data["company_id"])
#         ven_id = Vendor.objects.get(
#             vendor_id=debitnote_data["vendor_id"])
        
#         #account receivable varibale are declaret the chart of account of to side from item and taxation Section 
#         #and Discount time this chartof Account is From Side
       
#         # Invoice Item Looping
#         debitnote_item_list=[]
#         for debitnote_item_data in debitnote_data['debit_note_items']:
#            # Item are find Out Section
#             debitnote_item_list.append(debitnote_item_data['item_id'])
          
#             try:
#                 try:
#                     debitnote_item = DebitItem.objects.get(item_id=debitnote_item_data['item_id'],dn_id=debitnote.dn_id)
                    
#                 except KeyError:
#                     debitnote_item=None
                    
                  
                        
#             except DebitItem.DoesNotExist:
#                 debitnote_item=None
            
#             # Invoice Item Are Find the update this Code Section   
#             if debitnote_item is not None:
                
#                 item_serializer=DebitNoteItemSerializer(debitnote_item,data=debitnote_item_data)
#                 if item_serializer.is_valid():
#                     item_serializer.save()
#                 else:
#                     return Response(item_serializer.errors, status=400)
                   
#             else:
#                 try:
#                     # Get The Chart Of Account and item Id Of the Item Related
#                     coa=COA.objects.get(coa_id=debitnote_item_data["coa_id"])
#                     item=Item.objects.get(item_id=debitnote_item_data["item_id"])
#                 except KeyError:
#                     coa=None
#                     item=None
                
#                 try:
#                     #Item Does Not Exist Of Invoice item To Creating The Invoice Item Section
#                    debitnoteed_items = DebitItem.objects.create(dn_id=debitnote,
#                                                          item_id=Item.objects.get(
#                                                              item_id=debitnote_item_data["item_id"]),
#                                                          coa_id=COA.objects.get(
#                                                              coa_id=debitnote_item_data["coa_id"]),
#                                                          item_name=debitnote_item_data["item_name"],
#                                                          rate=debitnote_item_data["rate"],
#                                                          quantity=debitnote_item_data["quantity"],
#                                                          tax_rate=debitnote_item_data["tax_rate"],
#                                                          tax_name=debitnote_item_data["tax_name"],
#                                                          tax_type=debitnote_item_data["tax_type"],
#                                                          taxamount=debitnote_item_data["taxamount"],
#                                                          igst_amount=debitnote_item_data['igst_amount'],
#                                                          cgst_amount=debitnote_item_data['cgst_amount'],
#                                                          sgst_amount=debitnote_item_data['sgst_amount'],
#                                                          amount=debitnote_item_data["amount"])
#                 except KeyError:
#                     pass                 
                
                    
                
#         del_item = DebitItem.objects.filter(dn_id=debitnote.dn_id).exclude(item_id__in=debitnote_item_list).delete()      
#         #this Section Is Invoice Data Update Serializer Through
#         serializer = DebitnoteSerializer(debitnote, data=debitnote_data)

#         if serializer.is_valid():
#             debitnote_id=serializer.save()
            
#             # return Response({"data":serializer.data})
#         else:
#              return Response(serializer.errors, status=400)
         
         
#         stock_item_list=[]
#         stock_transactiom_item_list=[]
      
#         for debitnote_item_stock in debitnote_data['debit_note_items']:
#             stock_item_list.append(debitnote_item_stock['item_id'])
#             try:
#                 stock_item=Stock.objects.get(item_id=debitnote_item_stock['item_id'],ref_id=debitnote.dn_id)
#                 item_value=Item.objects.get(item_id=debitnote_item_stock["item_id"])
#                 current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                 # stock_serializer=StockSerializer(stock_item,data=invoice_item_data)
#                 print("updating stock", debitnote_item_stock['quantity'], debitnote_item_stock['item_id'])
#                 stock_item.stock_out=float (debitnote_item_stock['quantity'])
#                 stock_item.rate=float (current_assets_last_stock.rate)
#                 stock_item.amount=float(current_assets_last_stock.rate) * float(debitnote_item_stock['quantity'])
#                 stock_item.quantity=float (debitnote_item_stock['quantity'])
#                 stock_item.save()
#                 stock_transactiom_item_list.append(stock_item)
#             except Stock.DoesNotExist:
            
            
#                 item_value=Item.objects.get(item_id=debitnote_item_stock["item_id"])
#                 items_inventory=debitnote_data.get('debit_note_items')
#                 track_inventory=items_inventory[0].get('selected_item_name',{}).get('track_inventory')
#                 inv_item_coa=items_inventory[0].get('selected_item_name',{}).get('inventory_account')
                
#                 print('inventory item coa',inv_item_coa)
                        
#                 if track_inventory==True:
                    
        
#                     stk_in=Stock.objects.filter(item_id=debitnote_item_stock["item_id"]).exclude(stock_in=0).order_by('created_date')
#                     stk_out=Stock.objects.filter(item_id=debitnote_item_stock["item_id"]).exclude(stock_out=0).order_by('created_date')        
                
#                     print(stk_out)
#                     stock_int_items = stk_in
#                     already_stock_out_items =stk_out
#                     item_to_sell = debitnote_item_stock["quantity"]
#                     print('item_to_sell',item_to_sell)

#                     # -------------------------------------------------

#                     # Check if the stock is available
#                     sum_of_stock_in = sum([_.stock_in for _ in stock_int_items])
#                     print('sum of stock in',sum_of_stock_in)
#                     sum_of_stock_in_amount = sum([_.amount for _ in stock_int_items])
#                     print("sum_of_stock_in_amount", sum_of_stock_in_amount)

#                     sum_of_already_stock_out = sum([_.stock_out for _ in already_stock_out_items])
#                     print("sum_of_already_stock_out", sum_of_already_stock_out)

#                     if sum_of_stock_in - (sum_of_already_stock_out + item_to_sell) < 0:
#                         print("Stock not available")
#                         return Response('Stock Not Avilable')

#                     print("Stock available")
#                     current_stock=sum_of_stock_in-sum_of_already_stock_out
#                     print('item is herer',item_value.item_id)        
#                     current_assets_last_stock=Stock.objects.filter(item_id=item_value.item_id).latest('created_date')
#                     print("current Assets_vlaue",current_assets_last_stock.amount)
#                     future_stock_outs = []
#                     for stock_in_item in stock_int_items:
#                         print(stock_in_item)
                        
#                         if item_to_sell==0:
#                             print('Item Are not selled')
#                             break
#                         else:
#                             if sum_of_already_stock_out - stock_in_item.stock_in >= 0:
#                                 print("\tItem fully sold")
#                                 sum_of_already_stock_out = sum_of_already_stock_out - stock_in_item.stock_in
#                                 print("\tRemaining already sold items: ", sum_of_already_stock_out)
#                                 continue

#                             if sum_of_already_stock_out > 0:
#                                 print("\tItem partially unsold")
#                                 remaining_unsold_items = stock_in_item.stock_in - sum_of_already_stock_out
#                                 print("\tRemaining unsold items", remaining_unsold_items)
#                                 sum_of_already_stock_out = 0
#                             else:
#                                 print("\tItem fully unsold")
#                                 remaining_unsold_items = stock_in_item.stock_in
                            
#                             if item_to_sell > remaining_unsold_items:
#                                 print("\tMore items need to be sold")
#                                 print(f"\tSelling {remaining_unsold_items} items")
                                
#                                 future_stock_outs=Stock.objects.create(
#                                 item_id=debitnote_item_stock["item_id"],
#                                 item_name=debitnote_item_stock["item_name"],
#                                 stock_out=remaining_unsold_items,
#                                 ref_id=debitnote_id.dn_id,
#                                 amount=current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate,
#                                 rate=stock_in_item.rate,
#                                 ref_tblname='Debit Note',
#                                 quantity=remaining_unsold_items,
#                                 #stock_on_hand=current_stock-remaining_unsold_items,
#                                 formname='Debit Note',
#                                 module='Purchase',
#                                 stage='Add Stages',
#                                 date=debitnote_data["dn_date"],                
#                                 company_id=comp_id)
#                                 current_assets_last_stock.amount = current_assets_last_stock.amount- remaining_unsold_items*stock_in_item.rate
#                                 current_stock = current_stock-remaining_unsold_items
                                
                                    
#                                 #Stock(0, remaining_unsold_items, stock_in_item.rate)
#                                 item_to_sell = item_to_sell - remaining_unsold_items
#                                 print(f"\t{item_to_sell} still needed by the buyer")
#                             else:
#                                 print(f"\tSelling {item_to_sell} items")
#                                 future_stock_outs=Stock.objects.create(
#                                 item_id=debitnote_item_stock["item_id"],
#                                 item_name=debitnote_item_stock["item_name"],
#                                 stock_out=item_to_sell,
#                                 ref_id=debitnote_id.dn_id,
#                                 amount=current_assets_last_stock.amount- item_to_sell*stock_in_item.rate,
#                                 rate=stock_in_item.rate,
#                                 quantity=item_to_sell,
#                                 ref_tblname='DebitNote',
#                                 #stock_on_hand=current_stock-item_to_sell,
#                                 module='Purchase',
#                                 formname='Debit Note',
#                                 stage='Add Stages',
#                                 date=debitnote_data["dn_date"],                
#                                 company_id=comp_id)
                                
#                                 #append(Stock(0, item_to_sell, stock_in_item.rate))
#                                 item_to_sell = 0
                                


#             #This Section Is Stock Journal Transaction 
#             #Stock Charetd Account name is Inventory Assets
#                         # print('item rate',future_stock_outs.rate)
#                         # print('item quantity',future_stock_outs.quantity)
                        
#                             print('Journa created starts')
#                             account_payable =  COA.objects.get(company_id=comp_id,coa_id=inv_item_coa)
#                             TO_COA = COA.objects.get(company_id=comp_id, coa_id=debitnote_item_stock['coa_id'])
#                             stkmast = MasterTransaction.objects.create(
#                                 L1detail_id=debitnote_id.dn_id,
#                                 L1detailstbl_name='DebitNote',
#                                 L2detail_id=future_stock_outs.st_id,
#                                 L2detailstbl_name='Stock',
#                                 main_module='Purchase',
#                                 module='DebitNote',
#                                 sub_module='DebitNote',
#                                 transc_deatils='DebitNote',
#                                 banking_module_type='DebitNote',
#                                 journal_module_type='DebitNote',
#                                 trans_date=debitnote_data["dn_date"],
#                                 trans_status='Manually Added',
#                                 debit=future_stock_outs.rate*future_stock_outs.quantity,
#                                 to_account=TO_COA.coa_id,
#                                 to_acc_type=TO_COA.account_type,
#                                 to_acc_head=TO_COA.account_head,
#                                 to_acc_subhead=TO_COA.account_subhead,
#                                 to_acc_name=TO_COA.account_name,
#                                 credit=future_stock_outs.rate*future_stock_outs.quantity,
#                                 from_account=account_payable.coa_id,
#                                 from_acc_type=account_payable.account_type,
#                                 from_acc_head=account_payable.account_head,
#                                 from_acc_subhead=account_payable.account_subhead,
#                                 from_acc_name=account_payable.account_name,
#                                 company_id=comp_id,
#                                 vendor_id=ven_id)
#                             stkmast.save()
#                             print(stkmast.from_acc_type)
        
        
        
        
#         # 0%GST and 0%IGST Calculation
#         #0% Tax Is User Select
#         Zero_tax=debitnote_data.get('debit_note_items')
#         GST_TAX=None
#         if GST_TAX==Zero_tax[0]is not None:
#             GST_TAX=Zero_tax[0].get('selected_tax_name',{}).get('tax_name')
        
        
            
#         else:
#             pass
    

#         IGST_TAX=GST_TAX
#         if GST_TAX=='GST0 [0%]':
#             Both_Tax=GST_TAX   
            
#         else:
#             Both_Tax=None
           
#         if IGST_TAX=='IGST0 [0%]':
#             IGST_0=IGST_TAX
#         else:
#             IGST_0=None

#         transaction_list = [] #This Empty List added the append 
#         if float(debitnote_data['cgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Input CGST", "cgst_total"],)
#         if float(debitnote_data['sgst_total'])>0 or Both_Tax:
#             transaction_list.append(["Input SGST", "sgst_total"])
#         if float(debitnote_data['igst_total'])>0 or IGST_0:
#             transaction_list.append(["Input SGST", "igst_total"],)       
        
        
#         acc_from_list=[]
#         acc_to_list=[]
#         account_payable = COA.objects.get(company_id=comp_id, account_subhead='Account Payables')

#         for transaction in transaction_list:
               
#             for account_transaction in [transaction[0]]:
#                 acc_to_list.append(account_transaction)
#                 if account_transaction is not None:
#                     try:
#                         #this Section is List Addded Charted Of account Updated                
#                         account_list=MasterTransaction.objects.get(from_acc_name=account_transaction,L1detail_id=debitnote.dn_id)
#                         account_list.credit=debitnote_data[transaction[1]]
#                         account_list.debit=debitnote_data[transaction[1]]
#                         account_list.save()   
                   
#                     except MasterTransaction.DoesNotExist:
#                         FROM_COA = COA.objects.get(company_id=comp_id,account_name=transaction[0])
#                         dnmast = MasterTransaction.objects.create(
#                         L1detail_id=debitnote_id.dn_id,
#                         L1detailstbl_name='Debit Note',
#                         main_module='Purchase',
#                         module='Purchase',
#                         sub_module='DebitNote',
#                         transc_deatils='Debit Note Transaction',
#                         banking_module_type='Debit Note',
#                         journal_module_type='Debit Note',
#                         trans_date=debitnote_data["dn_date"],
#                         trans_status='Manually Added',
#                         debit=debitnote_data[transaction[1]],
#                         to_account=account_payable.coa_id,
#                         to_acc_type=account_payable.account_type,
#                         to_acc_head=account_payable.account_head,
#                         to_acc_subhead=account_payable.account_subhead,
#                         to_acc_name=account_payable.account_name,
#                         credit=debitnote_data[transaction[1]],
#                         from_account=FROM_COA.coa_id,
#                         from_acc_type=FROM_COA.account_type,
#                         from_acc_head=FROM_COA.account_head,
#                         from_acc_subhead=FROM_COA.account_subhead,
#                         from_acc_name=FROM_COA.account_name,
#                         company_id=comp_id,
#                         vendor_id=ven_id)
#                         dnmast.save()
            
                      
#         try:
#             #This Section is Disscount will Be find to this code will Be Excuted
#             try:
#                 discount_account=debitnote_data['discount_account']
#                 account_discount =COA.objects.get(company_id=comp_id, coa_id=discount_account)
#                 discount_acc_name=account_discount.account_name  
#                 item_discount_list=MasterTransaction.objects.get(to_acc_name=discount_acc_name,L1detail_id=debitnote.dn_id)
#                 print('discount list',item_discount_list)
#                 item_discount_list.credit=debitnote_data['discount']
#                 item_discount_list.debit=debitnote_data['discount']
#                 item_discount_list.save()
#                 print('discount Section is Updated Suessfully')
#             except:
#                 pass    
#         except MasterTransaction.DoesNotExist:
#             if float(debitnote_data['discount'])>0:
#                 discount_account=debitnote_data['discount_account']
#                 TO_COA =COA.objects.get(company_id=comp_id, coa_id=discount_account)
#                 discount_acc_name=TO_COA.account_name   
#                 acc_from_list.append(discount_acc_name)
#                 FROM_COA =COA.objects.get(coa_id=account_payable.coa_id)
#                 dnmast = MasterTransaction.objects.create(
#                     L1detail_id=debitnote_id.dn_id,
#                     L1detailstbl_name='Debit Note',
#                     main_module='Purchase',
#                     module='Purchase',
#                     sub_module='DebitNote',
#                     transc_deatils='Debit Note Transaction',
#                     banking_module_type='Debit Note',
#                     journal_module_type='Debit Note',
#                     trans_date=debitnote_data["dn_date"],
#                     trans_status='Manually Added',
#                     debit=debitnote_data['discount'],
#                     to_account=TO_COA.coa_id,
#                     to_acc_type=TO_COA.account_type,
#                     to_acc_head=TO_COA.account_head,
#                     to_acc_subhead=TO_COA.account_subhead,
#                     to_acc_name=TO_COA.account_name,
#                     credit=debitnote_data['discount'],
#                     from_account=FROM_COA.coa_id,
#                     from_acc_type=FROM_COA.account_type,
#                     from_acc_head=FROM_COA.account_head,
#                     from_acc_subhead=FROM_COA.account_subhead,
#                     from_acc_name=FROM_COA.account_name,
#                     company_id=comp_id,
#                     vendor_id=ven_id)
#                 dnmast.save()
#     #This Section is Item Transaction The Item transaction Can't Created Is only updated 
#     #this only Chnage the Credit and debit Side values 
#     #Other can;t Change



    
#         #This Section is Item chart of account and amount group by section
#         coa_amount_dict = {}       
#         for debit_item in debitnote_data['debit_note_items']:
#             if coa_amount_dict.get(debit_item['coa_id']) is None:
#                 coa_amount_dict[debit_item['coa_id']
#                                 ] = debit_item['amount']
#             else:
#                 coa_amount_dict[debit_item['coa_id']
#                                 ] = coa_amount_dict[debit_item['coa_id']] + debit_item['amount']
            
#             for coa_id, amount in coa_amount_dict.items():
              
#                 coa_mast=MasterTransaction.objects.filter(from_account=coa_id,L1detail_id=debitnote.dn_id)
#                 for coa in coa_mast:
                    
#                     coa_acc=coa.from_acc_name
                   
                   
      
#         trans_stock_list= Stock.objects.filter(ref_id=debitnote_id.dn_id).exclude(item_id__in=stock_item_list)
#         print('Start The item Is ready to delete',trans_stock_list)
#         for trans_stock in trans_stock_list:
#             mast_stock=trans_stock.st_id
#             transaction_stock= MasterTransaction.objects.filter(L1detail_id=debitnote_id.dn_id,L2detail_id=str(mast_stock)).delete()
#             print('Deleted Stock Transaction item Name is ',transaction_stock)
        
#         del_stock= Stock.objects.filter(ref_id=debitnote_id.dn_id).exclude(item_id__in=stock_item_list).delete()
#         print('Ohhh Stock is deleted',del_stock)
        
     
        
#       #this Section Is the Delete the Trnsaction Not Fined is List Mens Remove the Transaction
#         #master_stock variable is the remaning of stock item in master transaction
#         master_stock_list=[]
#         master_stock= MasterTransaction.objects.filter(L1detail_id=debitnote_id.dn_id,L2detailstbl_name='Stock')
#         for stock_trans_mast in master_stock:
#             master_stock_list.append(stock_trans_mast.to_acc_name)
#         print('acc toList Is here',acc_to_list)
#         print('acc fromList Is here',acc_from_list)
#         print('master_stock_list is herer',master_stock_list)
#         to_and_from=acc_from_list+acc_to_list
#         Both_List=to_and_from+master_stock_list
#         print('to_and_From is herer',to_and_from)
#         topics = MasterTransaction.objects.filter(L1detail_id=debitnote_id.dn_id,).exclude(to_acc_name__in=Both_List).exclude(from_acc_name__in=Both_List).delete()
#         print('Both List Is here',Both_List)
#         dn_item_list=DebitItem.objects.filter(dn_id=debitnote_id.dn_id,).exclude(item_id__in=stock_item_list).delete()

          
#         serializer = DebitnoteSerializer(debitnote_id)  # browser
#         return Response(serializer.data)
    
    
    