
from rest_framework.response import Response
from django.conf import settings
import razorpay
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from registration.models import Subscribe,SubscriptionOrder,Plan
from registration.serializers import SubscriptionOrderSerializer
from datetime import date
from django.shortcuts import redirect
from rest_framework import status
# Create your views here.
from django.db import transaction
class start_payment(APIView):

    @transaction.atomic
    def post(self,request):
        plan = request.data.get('plan_id',0)
        try:
            pl = Plan.objects.get(id=plan)
        except:
            return Response(status=404)
        amount = pl.price
        if amount:

            client = razorpay.Client(auth=(settings.PUBLIC_KEY, settings.SECRET_KEY))
            payment = client.order.create({"amount": int(amount) * 100,
                                           "currency": "INR",
                                           "payment_capture": "1"})
            sub = request.user.subscribe
            obj = SubscriptionOrder.objects.create(
                user=request.user,
                subscribe=sub,
                order_id=payment['id'],
                total_price=amount,
                currency="INR",
                plan=pl
            )
            serializer = SubscriptionOrderSerializer(obj)
            return Response(serializer.data)
        else:
            return Response(status=412)

class handle_payment_success(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def verify_signature(response_data,client):

        return client.utility.verify_payment_signature(response_data)

    @transaction.atomic
    def post(self,request):

        client = razorpay.Client(auth=(settings.PUBLIC_KEY, settings.SECRET_KEY))
        payment_id = request.data.get("razorpay_payment_id", "")
        provider_order_id = request.data.get("razorpay_order_id", "")
        signature_id = request.data.get("razorpay_signature", "")
        payment_object = client.payment.fetch(payment_id)
        print(payment_object)
        order = SubscriptionOrder.objects.get(order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.payment_method = payment_object['method']
        order.save()
        payment_status = payment_object['status']
        if payment_status == "captured":
            order.status = "APPROVED"
            today_date = date.today()
            order.subscribe.plan = order.plan
            # plan = order.plan
            # plan.update_service_count(order.subscribe.user_id)
            order.subscribe.total_price = order.total_price
            if order.subscribe.get_plan_subscribe():
                # order.start_date = order.subscribe.end_date
                # order.end_date = order.get_end_date(order.start_date)
                order.subscribe.start_date = today_date
                order.subscribe.end_date = order.get_end_date(today_date)
            else:
                # order.start_date = today_date
                order.subscribe.start_date = today_date
                order.subscribe.end_date = order.get_end_date(today_date)
                # order.end_date = order.get_end_date(today_date)

            order.subscribe.save()
            order.save()
            response = redirect('https://www.auto-counts.com')
            return response

        elif payment_status == 'failed':
            order.status = "DECLINED"
            order.save()
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)