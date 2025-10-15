from rest_framework import serializers
from .models import Beneficiary, Document, VerificationRecord, BlockchainHash

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class BeneficiarySerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Beneficiary
        fields = ['id','apaar_id','name','phone','state','verified','documents','created_at']

class VerificationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRecord
        fields = '__all__'
