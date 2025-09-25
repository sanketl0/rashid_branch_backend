import json
import os
import pandas as pd
import datetime
from pathlib import Path
from wsgiref.util import FileWrapper

from django.template.loader import get_template
from django.views.generic import View
from django.http import HttpResponse, FileResponse
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import api_view
from purchase.models.Tds_model import TDS
from purchase.serializers.Tds_serializers import tdsSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
#Tds Model View Sets
class tdsViewSet(viewsets.ModelViewSet):
    queryset = TDS.objects.all()
    serializer_class = tdsSerializer

#Tds List View
class tdsList(APIView):


    # @api_view Allow to define function that match http methods
    def get(self, request, comp_id,branch_id):
        tds = TDS.objects.filter(company_id=comp_id,branch_id=branch_id)
        serializer = tdsSerializer(tds, many=True)
        return Response(serializer.data)