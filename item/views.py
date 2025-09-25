from item.models.item_model import Item
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class TestUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        item = Item.objects.select_for_update().get(item_id=kwargs['item_id'])
        item.hsn_code = 1
        item.save()
        return Response({'status': 'updated'}, status=status.HTTP_200_OK)