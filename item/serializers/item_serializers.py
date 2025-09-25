from rest_framework import serializers
from item.models.item_model import Item,ItemGroup,ItemView
from item.models.stock_model import getstock_on_hand
from report.models import AccountBalance
from item.models.stock_model import Batch
from django.db.models import Q
from coa.models import COA

class ItemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemGroup
        fields = '__all__'
from django.db.models import Sum

class ItemSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['qr_code']

    def to_representation(self, instance):
        # Call the parent `to_representation` method to get the default representation
        data = super().to_representation(instance)
        total = Batch.objects.filter(item_id=instance.item_id).aggregate(total=Sum('stock_quantity'))
        data['stock_quantity'] = total['total'] if total['total'] else 0
        print( data['stock_quantity'])
        return data
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['qr_code']
        # depth=1

    def to_representation(self, instance):
        # Call the parent `to_representation` method to get the default representation
        data = super().to_representation(instance)
        i_name = None
        p_name = None
        s_name = None
        if instance.purchase_account:
            objs = COA.get_account(instance.purchase_account)
            if objs:
                p_name = objs.account_name
        if instance.sales_account:
            objs = COA.get_account(instance.sales_account)
            if objs:
                s_name = objs.account_name
        # data['state_tax_name'] = instance.state_tax.name if instance.state_tax else None
        # data['central_tax_name'] = instance.central_tax.name if instance.central_tax else None
        # if instance.inventory_account:
        #     objs = AccountBalance.objects.filter(coa_id=instance.inventory_account)
        #     if objs:
        #         i_name = objs[0].label
        # data['i_name'] = i_name
        data['p_name'] = p_name
        data['s_name'] = s_name
        # total = Batch.objects.filter(item_id=instance.item_id).aggregate(total=Sum('stock_quantity'))
        # data['stock_quantity'] = total['total'] if total['total'] else 0
        # print( data['stock_quantity'])
        return data

class ItemSerializer_v1(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['qr_code']


#This Serializer is used to expected item serializers    
class ShortItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemView
        fields = ['name','unit','cost_price','item_category','item_id','stock_quantity']



GstItem = [
    {"label": "Non-Taxable", "value": "Non-Taxable", "group": "non_tax_group"},
    {"label": "Out of Scope", "value": "Out of Scope", "group": "non_tax_group"},
    {"label": "Non-GST Supply", "value": "Non-GST Supply", "group": "non_tax_group"},
    {"label": "GST0 [0%]", "value": "0", "group": "state"},
    {"label": "GST5 [5%]", "value": "5", "group": "state"},
    {"label": "GST12 [12%]", "value": "12", "group": "state"},
    {"label": "GST18 [18%]", "value": "18", "group": "state"},
    {"label": "GST28 [28%]", "value": "28", "group": "state"},
]

IGstItem = [
  { "label": "IGST0 [0%]", "value": "0","group":"central" },
  { "label": "IGST5 [5%]", "value": "5" ,"group":"central"},
  { "label": "IGST12 [12%]", "value": "12" ,"group":"central"},
  { "label": "IGST18 [18%]", "value": "18" ,"group":"central"},
  { "label": "IGST28 [28%]", "value": "28" ,"group":"central"}
]

class ShortItemAllSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Extract custom arguments from kwargs
        self.branch_id = kwargs.pop('branch_id', None)

        # Initialize the parent class
        super(ShortItemAllSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Item
        fields = ['sales_account','purchase_account','sale_price','track_inventory','cost_price','item_id']
    def to_representation(self, instance):
        # Customize the representation of the serialized data
        representation = super().to_representation(instance)
        representation['label'] = instance.name
        representation['value'] = instance.item_id

        inter_rate = instance.inter_rate
        intra_rate = instance.intra_rate
        tax_rate= None
        tax_type = None
        tax_name = intra_rate
        i_tax_rate = None
        i_tax_type = None
        i_tax_name = inter_rate
        if intra_rate:
            filtered_items = list(filter(lambda x:x['label'] == tax_name,GstItem))
            if filtered_items:
                item = filtered_items[0]
                tax_rate = item['value']
                tax_type = item['group']
        representation['tax_name'] = tax_name
        representation['tax_rate'] = tax_rate
        representation['tax_type'] = tax_type
        if inter_rate:
            filtered_items = list(filter(lambda x:x['label'] == i_tax_name,IGstItem))
            if filtered_items:
                item = filtered_items[0]
                i_tax_rate = item['value']
                i_tax_type = item['group']
        representation['i_tax_name'] = i_tax_name
        representation['i_tax_rate'] = i_tax_rate
        representation['i_tax_type'] = i_tax_type
        stock_quantity = 0
        try:
            batch = Batch.objects.get(Q(item_id=instance.item_id,branch_id=self.branch_id,
                                        batch_no=None,expire_date=None,mfg_date=None))
            stock_quantity = batch.stock_quantity
        except Exception as e:
            print(e)

        print(self.branch_id,stock_quantity,instance.item_id)
        representation['stock_quantity'] = stock_quantity

        return representation
# serializer for get item short by company id with needed fields (v)
class GetItemShortByCompanyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'sale_price', 'unit', 'opening_stock_rate', 'item_category', 'item_id','opening_stock','coa_id']
        
        