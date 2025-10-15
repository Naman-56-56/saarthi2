from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import UserProfile

# Create your views here.

def signup(request):
    """Phone number signup page"""
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        
        if not phone:
            messages.error(request, 'Phone number is required')
            return render(request, 'signup.html')
        
        # Check if phone already exists
        existing_profile = UserProfile.objects.filter(phone=phone).first()
        
        if existing_profile:
            # User exists, send OTP again
            existing_profile.otp = '1234'  # Hardcoded OTP for demo
            existing_profile.save()
            request.session['signup_phone'] = phone
            messages.info(request, 'OTP sent to your phone')
            return redirect('verify_otp')
        
        # New user - create and send OTP
        request.session['signup_phone'] = phone
        request.session['signup_otp'] = '1234'  # Hardcoded OTP for demo
        messages.success(request, 'OTP sent to your phone')
        return redirect('verify_otp')
    
    return render(request, 'signup.html')


def verify_otp(request):
    """OTP verification page"""
    phone = request.session.get('signup_phone')
    
    if not phone:
        messages.error(request, 'Please enter your phone number first')
        return redirect('signup')
    
    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()
        
        if not otp:
            messages.error(request, 'OTP is required')
            return render(request, 'verify_otp.html', {'phone': phone})
        
        # Verify OTP (hardcoded as 1234)
        if otp != '1234':
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'verify_otp.html', {'phone': phone})
        
        # OTP is correct - create user if new
        profile = UserProfile.objects.filter(phone=phone).first()
        
        if not profile:
            # Create new user
            username = f"user_{phone}"
            user = User.objects.create_user(username=username)
            profile = UserProfile.objects.create(
                user=user,
                phone=phone,
                otp_verified=True
            )
        else:
            profile.otp_verified = True
            profile.save()
        
        # Log the user in
        login(request, profile.user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Clear session data
        request.session.pop('signup_phone', None)
        request.session.pop('signup_otp', None)
        
        messages.success(request, 'Successfully logged in!')
        return redirect('dashboard')
    
    return render(request, 'verify_otp.html', {'phone': phone})


def logout_view(request):
    """Logout user"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')
