from rest_framework import serializers
from item.models.manufacturing_journal import *
from item.models.stock_model import *
from coa.models import COA
from transaction.models import MasterTransaction
from django.db.models import Q
import traceback


class StockJournalConsumptionSer(serializers.ModelSerializer):
    quantity = serializers.CharField(required=False, allow_blank=True)
    batches = serializers.ListField()
    class Meta:
        model = Consumption
        exclude = ['cmp_id','sj_id']

    def validate_quantity(self, value):
        return float(value)

    def validate_quantity(self, value):
        return float(value)

    def to_representation(self, instance):
        # Call the parent `to_representation` method to get the default representation
        data = super().to_representation(instance)
        data['batches'] = eval(instance.batches)
        return data


class StockJournalConsumptionProd(serializers.ModelSerializer):
    quantity = serializers.CharField(required=False, allow_blank=True)
    batches = serializers.ListField()
    class Meta:
        model = Production
        exclude = ['prd_id','sj_id']

    def validate_quantity(self, value):
        return float(value)

    def validate_batches(self, value):
        return value
    def to_representation(self, instance):
        # Call the parent `to_representation` method to get the default representation
        data = super().to_representation(instance)
        data['batches'] = eval(instance.batches)
        return data
class StockJournalSerializer(serializers.ModelSerializer):
    consumption_items = StockJournalConsumptionSer(many=True)
    production_items = StockJournalConsumptionProd(many=True)

    class Meta:
        model = StockJournal
        exclude = ['sj_id']

    @staticmethod
    def create_journal(consumption_items, production_items,
                                   instance, validated_data):

        branch_id = validated_data['branch_id'].branch_id
        company_id = validated_data['company_id'].company_id
        ext_id = validated_data.get('ext_id',None)
        cmp_stocks = Stock.objects.filter(
            ref_id=instance.sj_id,
            ref_tblname='Stock Journal',
            formname='Stock Cmp Journal',
            branch_id=instance.branch_id,
            company_id=instance.company_id,
            stage='Add Stages'
        )
        prev_stk_list = {(stock.item_id, stock.batch_no, stock.expire_date, stock.mfg_date,float(stock.quantity),stock.godown_id_id): stock for stock in
                         cmp_stocks}
        cmp_stk_list = {}
        for cmp_item in consumption_items:
            godown_id = cmp_item['godown_id']
            print(godown_id.wh_id,">>>>>>>>>>>>>>>>",cmp_item['godown_name'],"?????????????????")
            Consumption.objects.create(
                sj_id=instance,
                **cmp_item
            )
            item_obj = cmp_item["item_id"]
            cmp_item_amount = float(cmp_item["amount"])
            cmp_rate = float(cmp_item["rate"])
            track_inventory = item_obj.track_inventory
            if track_inventory:
                batches = cmp_item['batches']
                mfg_date = cmp_item['mfg_date']
                expire_date = cmp_item['expire_date']
                if len(batches) == 0:
                    batches.append(None)
                    mfg_date = None
                    expire_date = None
                stk_in = None
                stk_out = None
                remaining_to_sell = float(cmp_item["quantity"])
                for index, batch in enumerate(batches):
                    obj_cmp, created = Stock.objects.get_or_create(
                        item_id=item_obj.item_id,

                        ref_id=instance.sj_id,
                        ref_tblname='Stock Journal',
                        formname='Stock Cmp Journal',
                        expire_date=expire_date,
                        mfg_date=mfg_date,
                        quantity=float(round(cmp_item["quantity"],2)),
                        batch_no=batch,
                        godown_id=godown_id,
                        branch_id=instance.branch_id,
                        company_id=instance.company_id,
                        stage='Add Stages',
                        module="Item"
                    )
                    if remaining_to_sell > 0:
                        if False:
                            if batch is None:
                                try:
                                    batch_total_stk_in = Batch.objects.get(Q(item_id=item_obj.item_id,
                                                                             expire_date=expire_date,
                                                                             mfg_date=mfg_date,
                                                                             branch_id=branch_id,
                                                                             batch_no__isnull=True))
                                except Exception as e:
                                    print(f"name => {cmp_item['item_name']} , "
                                          f"item_id => {item_obj.item_id}, "
                                          f"batch_no => {batch} ,remaining => {remaining_to_sell},"
                                          f"qty => {cmp_item['quantity']}")
                                    raise Exception("Batch Item not available")
                                batch_total_stk_in = float(batch_total_stk_in.stock_quantity)

                            else:

                                try:
                                    batch_total_stk_in = Batch.objects.get(item_id=item_obj.item_id,
                                                                           expire_date=expire_date,
                                                                           mfg_date=mfg_date,
                                                                           branch_id=branch_id,
                                                                           batch_no=batch)
                                    batch_total_stk_in = float(batch_total_stk_in.stock_quantity)
                                except Exception as e:
                                    print(e, "error")
                                    print(f"name => {cmp_item['item_name']} , "
                                          f"item_id => {item_obj.item_id}, branch_id => {branch_id} {expire_date} => {mfg_date}"
                                          f"batch_no => {batch} ,remaining => {remaining_to_sell},"
                                          f"qty => {cmp_item['quantity']},"
                                          )
                                    raise Exception("Batch Item not available")
                            if not created:
                                batch_total_stk_in += float(obj_cmp.quantity)
                            if index == len(batches) - 1:
                                if (batch_total_stk_in - remaining_to_sell) < 0:
                                    print(f"name => {cmp_item['item_name']} , "
                                          f"item_id => {item_obj.item_id}, "
                                          f"batch_no => {batch} ,remaining => {remaining_to_sell},"
                                          f"qty => {cmp_item['quantity']},"
                                          f"batch_qty => {batch_total_stk_in}")
                                    raise Exception("Stock Not Available")
                        obj_cmp.godown_name = cmp_item['godown_name']
                        obj_cmp.flow_type = 'OUTWARD'
                        obj_cmp.item_name = cmp_item["item_name"]
                        obj_cmp.stock_out = cmp_item['quantity']
                        obj_cmp.stock_in = 0
                        obj_cmp.amount = cmp_item_amount
                        obj_cmp.rate = cmp_rate
                        obj_cmp.module_date = instance.created_date
                        obj_cmp.date = instance.date
                        obj_cmp.save()
                        print(obj_cmp.godown_name,"xxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                        cmp_stk_list[(obj_cmp.item_id, obj_cmp.batch_no, obj_cmp.expire_date, obj_cmp.mfg_date,
                                      float(obj_cmp.quantity),obj_cmp.godown_id_id)] = obj_cmp


        for key, obj in prev_stk_list.items():
            if key not in cmp_stk_list:
                print("deleting child")
                obj.delete()
        prod_stocks = Stock.objects.filter(
            ref_id=instance.sj_id,
            ref_tblname='Stock Journal',
            formname='Stock Prod Journal',
            branch_id=instance.branch_id,
            company_id=instance.company_id,
            stage='Add Stages'
        )
        prev_stk_list = {(stock.item_id, stock.batch_no, stock.expire_date, stock.mfg_date,float(stock.quantity),stock.godown_id_id): stock for stock in
                         prod_stocks}
        prod_stk_list = {}
        for prod_item in production_items:
            godown_id = prod_item['godown_id']
            if godown_id:
                godown_id = godown_id.wh_id
            else:
                godown_id = None
            Production.objects.create(
                sj_id=instance,
                **prod_item
            )
            item_obj = prod_item["item_id"]
            track_inventory = item_obj.track_inventory
            prod_rate = prod_item["rate"]
            prod_item_amount= prod_item["amount"]
            if track_inventory:
                batch = prod_item["batches"]
                exp_date = prod_item["expire_date"]
                mfg_date = prod_item["mfg_date"]
                if not batch:
                    batch.append(None)
                    exp_date = None
                    mfg_date = None
                if prod_rate <= 0:
                    prod_item_amount = 0
                t_amount = round(float(prod_item_amount),2)
                obj_prod, created = Stock.objects.get_or_create(
                    item_id=item_obj.item_id,
                    ref_id=instance.sj_id,
                    ref_tblname='Stock Journal',
                    formname='Stock Prod Journal',
                    expire_date=exp_date,
                    quantity=float(round(prod_item['quantity'],2)),
                    mfg_date=mfg_date,
                    batch_no=batch[0],
                    godown_id_id=godown_id,
                    branch_id=instance.branch_id,
                    company_id=instance.company_id,
                    stage='Add Stages',
                    module="Item"
                )
                obj_prod.godown_name = prod_item['godown_name']
                obj_prod.flow_type = 'INWARD'
                obj_prod.item_name = prod_item["item_name"]
                obj_prod.stock_in = prod_item['quantity']
                obj_prod.stock_out = 0
                obj_prod.module_date = instance.created_date
                obj_prod.amount = t_amount
                obj_prod.rate = prod_rate

                obj_prod.date = instance.date
                obj_prod.save()
                prod_stk_list[(obj_prod.item_id, obj_prod.batch_no, obj_prod.expire_date,
                               obj_prod.mfg_date,float(obj_prod.quantity),obj_prod.godown_id_id)] = obj_prod
        for key, obj in prev_stk_list.items():
            if key not in prod_stk_list:
                print("deleting child")
                obj.delete()

        return instance

    def create(self, validated_data):
        consumption_items = validated_data.pop('consumption_items')
        production_items = validated_data.pop('production_items')

        instance = StockJournal.objects.create(
            **validated_data
        )
        return self.create_journal(consumption_items, production_items,
                                   instance, validated_data)

    def update(self, instance, validated_data):
        consumption_items = validated_data.pop('consumption_items')
        production_items = validated_data.pop('production_items')
        instance.__dict__.update(validated_data)
        instance.save()

        return self.create_journal(consumption_items,production_items,instance,validated_data)

class StockJournalManySerializer(serializers.ModelSerializer):

    class Meta:
        model = StockJournal
        fields = '__all__'

class StockJournalGetSerializer(serializers.ModelSerializer):
    consumption_items = StockJournalConsumptionSer(many=True)
    production_items = StockJournalConsumptionProd(many=True)

    class Meta:
        model = StockJournal
        exclude = ['sj_id']

    def to_representation(self, instance):
        # Call the parent `to_representation` method to get the default representation
        data = super().to_representation(instance)
        return data

class ManufacturingByItemSerializer(serializers.ModelSerializer):
    batches = serializers.ListField()
    quantity = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = ManufacturingByItem
        exclude = ['mfg_id']

    def validate_batches(self, value):
        return value
    def validate_quantity(self, value):
        return float(value)
    def to_representation(self, instance):
        # Call the parent `to_representation` method to get the default representation
        data = super().to_representation(instance)
        data['batches'] = eval(instance.batches)
        return data


class ManufacturingJournalItemSerializer(serializers.ModelSerializer):
    batches = serializers.ListField()
    quantity = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = ManufacturingJournalItem
        exclude = ['mfg_id']

    def validate_batches(self, value):
        print("validate_batches called")  # Debugging print statement
        return value
    def validate_quantity(self, value):
        return float(value)
    def to_representation(self, instance):
        # Call the parent `to_representation` method to get the default representation
        data = super().to_representation(instance)

        data['batches'] = eval(instance.batches)

        return data

class MfgGetSerializer(serializers.ModelSerializer):
    mfg_items = ManufacturingJournalItemSerializer(many=True)
    mfg_by_items = ManufacturingByItemSerializer(many=True)

    class Meta:
        model = ManufacturingJournal
        exclude = ['mfg_id']

    def to_representation(self, instance):
        # Call the parent `to_representation` method to get the default representation
        data = super().to_representation(instance)

        data['batches'] = eval(instance.batches)
        return data


class MfgManySerializer(serializers.ModelSerializer):

    class Meta:
        model = ManufacturingJournal
        fields = '__all__'


class MfgSerializer(serializers.ModelSerializer):
    mfg_items = ManufacturingJournalItemSerializer(many=True)
    mfg_by_items = ManufacturingByItemSerializer(many=True)
    batches = serializers.ListField()
    total_stock = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = ManufacturingJournal
        fields = '__all__'

    def validate_batches(self, value):
        return value

    def validate_total_stock(self, value):
        return float(value)

    def create_mfg_journal(self,mfg_items,mfg_by_items,validated_data,instance):
        branch_id = validated_data['branch_id'].branch_id
        ext_id = validated_data.get('ext_id',None)
        stocks = Stock.objects.filter(
            item_id=instance.item_id.item_id,
            item_name=instance.item_name,
            ref_id=instance.mfg_id,
            ref_tblname='Manufacture',
            formname='Manufacture',
            expire_date=instance.expire_date,
            mfg_date=instance.mfg_date,
            godown_id=instance.godown_id,
            batch_no=instance.batches[0] if instance.batches else None,
            branch_id=instance.branch_id,
            company_id=instance.company_id,
            stage='Add Stages'
        )
        stk_list = {(stock.item_id, stock.batch_no, stock.expire_date, stock.mfg_date,stock.godown_id_id): stock for stock in stocks}
        obj,created = Stock.objects.get_or_create(
            item_id=instance.item_id.item_id,
            godown_id=instance.godown_id,
            ref_id=instance.mfg_id,
            ref_tblname='Manufacture',
            formname='Manufacture',
            expire_date=instance.expire_date,
            mfg_date=instance.mfg_date,
            batch_no=instance.batches[0] if instance.batches else None,
            branch_id=instance.branch_id,
            company_id=instance.company_id,
            stage='Add Stages'
        )
        obj.flow_type = 'INWARD'
        obj.godown_name = instance.godown_name
        obj.item_name=instance.item_name
        obj.stock_in = instance.total_stock
        obj.stock_out = 0
        obj.module_date = instance.created_date
        obj.amount = instance.effective_cost
        obj.rate = instance.effective_rate
        obj.quantity = instance.total_stock
        obj.date = instance.journal_date
        obj.save()
        current_lst = [(str(instance.item_id.item_id), instance.batches[0] if instance.batches else None,
                        instance.expire_date, instance.mfg_date,instance.godown_id_id)]
        for key, obj in stk_list.items():
            if key not in current_lst:
                print("deleting child")
                obj.delete()
        mfg_stocks = Stock.objects.filter(
            ref_id=instance.mfg_id,
            ref_tblname='Manufacture',
            formname='Consumption Item',
            branch_id=instance.branch_id,
            company_id=instance.company_id,
            stage='Add Stages'
        )
        prev_stk_list = {(stock.item_id, stock.batch_no, stock.expire_date, stock.mfg_date,stock.godown_id_id): stock for stock in mfg_stocks}
        mfg_stk_list = {}
        for mfg_item in mfg_items:
            godown_id = mfg_item['godown_id']
            if godown_id:
                godown_id = godown_id.wh_id
            else:
                godown_id = None
            print(mfg_item, ">>>>>>>>>>>>>>")
            ManufacturingJournalItem.objects.create(
                mfg_id=instance,
                **mfg_item
            )
            item_obj = mfg_item["item_id"]
            mfg_item_amount = mfg_item["amount"]
            mfg_rate = float(mfg_item['rate'])
            mfg_qty = float(mfg_item['quantity'])
            track_inventory = item_obj.track_inventory
            if track_inventory:
                batches = mfg_item['batches']
                mfg_date = mfg_item['mfg_date']
                expire_date = mfg_item['expire_date']
                if len(batches) == 0:
                    batches.append(None)
                    mfg_date = None
                    expire_date = None
                remaining_to_sell = float(mfg_item["quantity"])

                for index, batch in enumerate(batches):
                    obj_mfg, created = Stock.objects.get_or_create(
                        item_id=item_obj.item_id,
                        godown_id_id=godown_id,
                        ref_id=instance.mfg_id,
                        ref_tblname='Manufacture',
                        formname='Consumption Item',
                        expire_date=expire_date,
                        mfg_date=mfg_date,
                        batch_no=batch,
                        branch_id=instance.branch_id,
                        company_id=instance.company_id,
                        stage='Add Stages'
                    )
                    if remaining_to_sell > 0:
                        if False:
                            if batch is None:
                                try:
                                    batch_total_stk_in = Batch.objects.get(Q(item_id=item_obj.item_id,
                                                                             expire_date=expire_date,
                                                                             mfg_date=mfg_date,
                                                                             branch_id=branch_id,
                                                                             batch_no__isnull=True))
                                except Exception as e:
                                    raise Exception("Batch Item not available")
                                batch_total_stk_in = float(batch_total_stk_in.stock_quantity)

                            else:

                                try:
                                    batch_total_stk_in = Batch.objects.get(item_id=item_obj.item_id,
                                                                           expire_date=expire_date,
                                                                           mfg_date=mfg_date,
                                                                           branch_id=branch_id,
                                                                           batch_no=batch)
                                except Exception as e:
                                    print(e, "error")
                                    raise Exception("Batch Item not available")
                                batch_total_stk_in = float(batch_total_stk_in.stock_quantity)
                                print(item_obj, item_obj.item_id, branch_id, batch, mfg_date, expire_date)
                            if not created:
                                batch_total_stk_in += float(obj_mfg.quantity)
                            if index == len(batches) - 1:

                                if (batch_total_stk_in - remaining_to_sell) < 0:
                                    print(remaining_to_sell, batch_total_stk_in)
                                    raise Exception("Stock Not Available")
                        obj_mfg.flow_type = 'OUTWARD'
                        obj_mfg.godown_name = mfg_item['godown_name']
                        obj_mfg.item_name=mfg_item["item_name"]
                        obj_mfg.stock_out = mfg_qty
                        obj_mfg.stock_in = 0
                        obj_mfg.amount = mfg_item_amount
                        obj_mfg.module_date = instance.created_date
                        obj_mfg.rate = mfg_rate
                        obj_mfg.quantity = mfg_qty
                        obj_mfg.date = instance.journal_date
                        obj_mfg.save()
                        mfg_stk_list[(obj_mfg.item_id, obj_mfg.batch_no, obj_mfg.expire_date, obj_mfg.mfg_date,obj_mfg.godown_id_id)] = obj_mfg


        for key, obj in prev_stk_list.items():
            if key not in mfg_stk_list:
                print("deleting child")
                obj.delete()

        by_stocks = Stock.objects.filter(
            ref_id=instance.mfg_id,
            ref_tblname='Manufacture',
            formname='By Item',
            branch_id=instance.branch_id,
            company_id=instance.company_id,
            stage='Add Stages'
        )
        prev_stk_list = {(stock.item_id, stock.batch_no, stock.expire_date, stock.mfg_date,stock.godown_id_id): stock for stock in
                         by_stocks}
        by_stk_list = {}
        for mfg_by_item in mfg_by_items:
            godown_id = mfg_by_item['godown_id']
            if godown_id:
                godown_id = godown_id.wh_id
            else:
                godown_id = None
            ManufacturingByItem.objects.create(
                mfg_id=instance,
                **mfg_by_item
            )
            item_obj = mfg_by_item["item_id"]
            track_inventory = item_obj.track_inventory
            if track_inventory:
                batch = mfg_by_item["batches"]
                exp_date = mfg_by_item["expire_date"]
                mfg_date = mfg_by_item["mfg_date"]
                if not batch:
                    batch.append(None)
                    exp_date = None
                    mfg_date = None

                obj_by, created = Stock.objects.get_or_create(
                    item_id=item_obj.item_id,
                    godown_id_id=godown_id,
                    ref_id=instance.mfg_id,
                    ref_tblname='Manufacture',
                    formname='By Item',
                    expire_date=exp_date,
                    mfg_date=mfg_date,
                    batch_no=batch[0],
                    branch_id=instance.branch_id,
                    company_id=instance.company_id,
                    stage='Add Stages'
                )
                obj_by.flow_type = 'INWARD'
                obj_by.godown_name = mfg_by_item['godown_name']
                obj_by.item_name=mfg_by_item["item_name"]
                obj_by.stock_in = mfg_by_item["quantity"]
                obj_by.stock_out = 0
                obj_by.amount = round(float(mfg_by_item['amount']), 2)
                obj_by.rate = mfg_by_item["rate"]
                obj_by.quantity = mfg_by_item["quantity"]
                obj_by.date = instance.journal_date
                obj_by.module_date = instance.created_date
                obj_by.save()
                by_stk_list[(obj_by.item_id, obj_by.batch_no, obj_by.expire_date, obj_by.mfg_date,obj_by.godown_id_id)] = obj_by

        for key, obj in prev_stk_list.items():
            if key not in by_stk_list:
                print("deleting child")
                obj.delete()



    def create(self,validated_data):
        mfg_items = validated_data.pop('mfg_items')
        mfg_by_items = validated_data.pop('mfg_by_items')
        instance = ManufacturingJournal.objects.create(
            **validated_data
        )
        self.create_mfg_journal(mfg_items,mfg_by_items,validated_data,instance)
        return instance


    def update(self, instance, validated_data):
        mfg_items = validated_data.pop('mfg_items')
        mfg_by_items = validated_data.pop('mfg_by_items')
        instance.__dict__.update(validated_data)

        self.create_mfg_journal(mfg_items, mfg_by_items, validated_data, instance)
        return instance