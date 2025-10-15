from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import hashlib
import json

class Beneficiary(models.Model):
    # core profile
    apaar_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    caste_certificate = models.CharField(max_length=256, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.apaar_id} - {self.name or 'Unknown'}"

class Document(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, related_name='documents', on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=50)  # e.g., 'caste_cert', 'income_proof'
    file_url = models.CharField(max_length=512)  # store path or URL
    uploaded_at = models.DateTimeField(auto_now_add=True)

class VerificationRecord(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, related_name='verifications', on_delete=models.CASCADE)
    # raw_verification_data should be small or JSON string
    raw_data = models.JSONField(null=True, blank=True)
    trust_score = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, default='pending')  # pending, success, manual_review, failed
    created_at = models.DateTimeField(auto_now_add=True)

class BlockchainHash(models.Model):
    verification = models.OneToOneField(VerificationRecord, related_name='blockchain', on_delete=models.CASCADE)
    hash = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_hash(verification: VerificationRecord):
        payload = {
            'beneficiary': verification.beneficiary.apaar_id,
            'trust_score': verification.trust_score,
            'status': verification.status,
            'timestamp': verification.created_at.isoformat()
        }
        s = json.dumps(payload, sort_keys=True).encode('utf-8')
        return hashlib.sha256(s).hexdigest()
