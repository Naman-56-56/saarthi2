from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from api.models import VerificationRecord, Beneficiary

# Create your views here.

@login_required
def dashboard(request):
    """User dashboard - shows user info and verification history"""
    user = request.user
    profile = getattr(user, 'profile', None)
    
    # Get user's verification attempts (matching by phone)
    verification_attempts = []
    if profile and profile.phone:
        # Find beneficiaries with the same phone
        beneficiaries = Beneficiary.objects.filter(phone=profile.phone)
        for ben in beneficiaries:
            verifications = VerificationRecord.objects.filter(beneficiary=ben).order_by('-created_at')
            for ver in verifications:
                verification_attempts.append({
                    'apaar_id': ben.apaar_id,
                    'name': ben.name,
                    'trust_score': ver.trust_score,
                    'status': ver.status,
                    'created_at': ver.created_at
                })
    
    context = {
        'user': user,
        'profile': profile,
        'verification_attempts': verification_attempts
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def verify_apaar(request):
    """APAAR verification page"""
    return render(request, 'verify_apaar.html')
