from django.shortcuts import render

# Create your views here.
from . import models
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Beneficiary, Document, VerificationRecord, BlockchainHash
from .serializers import BeneficiarySerializer, VerificationRecordSerializer, DocumentSerializer
from rest_framework import status
from django.utils import timezone

# MOCK APAAR verification - replace with actual DigiLocker API integration later
def apaar_verify_mock(apaar_id):
    # simple whitelist
    valid = {"APAAR123": {"name":"Raju Kumar","state":"UP"},
             "VALID123": {"name":"Sita Devi","state":"Bihar"}}
    return valid.get(apaar_id)

# Simple scoring function — replace with ML pipeline later
def compute_trust_score(verification_data: dict) -> float:
    # Dummy scoring rules:
    # +40 if identity verified
    # +30 if caste cert present
    # +remaining from heuristics: ration usage, DBT present, education level...
    score = 0.0
    if verification_data.get('identity_verified'):
        score += 40
    if verification_data.get('caste_certificate'):
        score += 30
    # heuristics:
    score += min(30, verification_data.get('evidence_score', 0))
    # clamp
    return round(min(100, score), 2)

@api_view(['POST'])
@permission_classes([AllowAny])
def apply_beneficiary(request):
    """
    Endpoint: POST /api/apply/
    payload: { apaar_id, phone, name (optional) }
    """
    apaar_id = request.data.get('apaar_id')
    phone = request.data.get('phone')
    name = request.data.get('name', '')
    if not apaar_id or not phone:
        return Response({'detail': 'apaar_id and phone required'}, status=400)
    obj, created = Beneficiary.objects.get_or_create(apaar_id=apaar_id, defaults={'phone':phone,'name':name})
    if not created:
        obj.phone = phone
        if name:
            obj.name = name
        obj.save()
    ser = BeneficiarySerializer(obj)
    return Response(ser.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_document(request):
    """
    Minimal doc upload for demo. In real app, files would go to S3 or server storage.
    POST body: { apaar_id, doc_type, file_url }
    """
    apaar_id = request.data.get('apaar_id')
    doc_type = request.data.get('doc_type')
    file_url = request.data.get('file_url')
    if not apaar_id or not doc_type or not file_url:
        return Response({'detail':'apaar_id, doc_type, file_url required'}, status=400)
    ben = get_object_or_404(Beneficiary, apaar_id=apaar_id)
    doc = Document.objects.create(beneficiary=ben, doc_type=doc_type, file_url=file_url)
    return Response(DocumentSerializer(doc).data, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_apaar(request):
    """
    POST /api/verify-apaar/
    JSON: { "apaar_id": "APAAR123", "name": "Ravi Kumar", "income": 6500, "education_level": "High School", "location": "Patna, Bihar" }
    """
    # Read from JSON body
    apaar_id = request.data.get('apaar_id')
    name = request.data.get('name')
    income = request.data.get('income')
    education_level = request.data.get('education_level')
    location = request.data.get('location')

    if not apaar_id:
        return Response({'status': 'error', 'message': 'APAAR ID not provided'}, status=400)

    data = apaar_verify_mock(apaar_id)
    if not data:
        return Response({'status': 'error', 'message': 'Invalid APAAR ID'}, status=404)

    ben, _ = Beneficiary.objects.get_or_create(
        apaar_id=apaar_id,
        defaults={'name': data.get('name', name), 'state': data.get('state', location)}
    )

    heur = {
        'identity_verified': True,
        'caste_certificate': bool(getattr(ben, 'caste_certificate', False)),
        'evidence_score': 10
    }

    score = compute_trust_score(heur)
    vr = VerificationRecord.objects.create(
        beneficiary=ben,
        raw_data={'identity': data, 'heuristics': heur},
        status='success' if score >= 60 else 'manual_review',
        trust_score=score
    )

    h = BlockchainHash.create_hash(vr)
    BlockchainHash.objects.create(verification=vr, hash=h)

    return Response({
        'status': 'success',
        'message': f'APAAR {apaar_id} verified successfully',
        'trust_score': score,
        'status_flag': vr.status
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_manual_score(request):
    """
    Admin endpoint to re-run scoring with more data.
    POST { verification_id }
    """
    vid = request.data.get('verification_id')
    vr = get_object_or_404(VerificationRecord, id=vid)
    # combine documents / external checks (mocked)
    docs = list(vr.beneficiary.documents.values('doc_type','file_url'))
    evidence_score = 10 + len(docs)*10
    heur = {'identity_verified': True, 'caste_certificate': any(d['doc_type']=='caste_cert' for d in docs), 'evidence_score': evidence_score}
    score = compute_trust_score(heur)
    vr.trust_score = score
    vr.status = 'success' if score>=60 else 'manual_review'
    vr.raw_data.update({'heuristics': heur, 'docs': docs})
    vr.save()
    # update blockchain
    bc = getattr(vr,'blockchain',None)
    if bc:
        bc.hash = BlockchainHash.create_hash(vr)
        bc.save()
    else:
        BlockchainHash.objects.create(verification=vr, hash=BlockchainHash.create_hash(vr))
    return Response({'ok':True, 'trust_score':score, 'status':vr.status})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    """
    Simple admin stats endpoint
    """
    total = Beneficiary.objects.count()
    verified = VerificationRecord.objects.filter(status='success').count()
    pending = VerificationRecord.objects.filter(status='manual_review').count()
    avg_score = VerificationRecord.objects.all().aggregate(models.Avg('trust_score'))['trust_score__avg'] or 0
    return Response({
        'total_beneficiaries': total,
        'verified_count': verified,
        'pending_reviews': pending,
        'avg_trust_score': round(avg_score,2)
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def batch_sync(request):
    """
    Accepts a batch of offline-submitted applications from field devices.
    Payload: { batch: [ {apaar_id, phone, name, docs: [{doc_type,file_url}] }, ... ] }
    """
    batch = request.data.get('batch', [])
    results = []
    for item in batch:
        apaar_id = item.get('apaar_id')
        phone = item.get('phone')
        name = item.get('name','')
        ben, created = Beneficiary.objects.get_or_create(apaar_id=apaar_id, defaults={'phone':phone,'name':name})
        # create docs
        for d in item.get('docs', []):
            Document.objects.get_or_create(beneficiary=ben, doc_type=d.get('doc_type'), file_url=d.get('file_url'))
        # create verification record
        vr = VerificationRecord.objects.create(beneficiary=ben, status='pending', raw_data={'origin':'batch_sync','submitted_at': timezone.now().isoformat()})
        results.append({'apaar_id':apaar_id, 'verification_id': vr.id})
    return Response({'imported': len(results), 'results': results})
