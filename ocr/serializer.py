from rest_framework import serializers
from ocr.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    class Meta:
        model = Document
        fields = ['created_date','doc_id','filename', 'error', 'error_message','time_required','status']



class DocumentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['created_date','filename', 'error', 'error_message','time_required','status','result']


class DocumentQSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["doc_id"]