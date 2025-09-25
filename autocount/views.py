from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from registration.models import user
from registration.serializers import UsersGetSerializer

class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        """
        Check that the start date is before the end date.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data

class UserDashboardView(APIView):

    def post(self,request):
        data = request.data

        serializer = DateRangeSerializer(data=data)
        if serializer.is_valid():
            objs = user.objects.filter(created_date__range=[data['start_date'],data['end_date']])
            ser = UsersGetSerializer(objs,many=True)
            return Response(ser.data,status=200)

        return Response(status=400)