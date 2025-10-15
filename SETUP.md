# Quick Start Guide - SAARTHI Platform

## Setup Steps

### 1. Activate Virtual Environment & Navigate to Project
```powershell
cd "C:\Users\Naman Sharma\Documents\Django Projects\saarthi2"
.\env\Scripts\activate
cd saarthi2
```

### 2. Run Development Server
```powershell
python manage.py runserver
```

### 3. Access the Application
Open your browser and go to: **http://localhost:8000/**

---

## Testing the Application

### Step 1: Homepage
- Visit http://localhost:8000/
- You'll see the SAARTHI landing page with features
- Click "Sign Up Now"

### Step 2: Sign Up
- Enter any 10-digit phone number (e.g., `9876543210`)
- Click "Send OTP"

### Step 3: Verify OTP
- Enter OTP: **1234**
- Click "Verify & Login"
- You'll be redirected to the dashboard

### Step 4: Dashboard
- View your user info and phone number
- Click "Verify APAAR ID" button

### Step 5: APAAR Verification
- Use one of these demo APAAR IDs:
  - **APAAR123**
  - **VALID123**
- Fill in the form:
  - Name: Any name
  - Income: Any number (e.g., 5000)
  - Education: Select from dropdown
  - Location: Any location (e.g., "Delhi, India")
- Click "Verify APAAR ID"
- View the verification result with trust score

### Step 6: Check History
- Click "Back to Dashboard"
- Scroll down to see your verification history in the table

---

## Demo Credentials Summary

| Field | Value |
|-------|-------|
| Phone Number | Any 10 digits (e.g., 9876543210) |
| OTP | **1234** |
| Valid APAAR IDs | **APAAR123** or **VALID123** |

---

## Admin Panel (Optional)

### Create Superuser
```powershell
python manage.py createsuperuser
```

### Access Admin
- URL: http://localhost:8000/admin/
- View and manage:
  - Users
  - User Profiles
  - Beneficiaries
  - Verification Records
  - Blockchain Hashes

---

## URL Routes

| Page | URL | Auth Required |
|------|-----|---------------|
| Homepage | `/` | No |
| Sign Up | `/signup/` | No |
| Verify OTP | `/verify-otp/` | No |
| Dashboard | `/dashboard/` | Yes |
| APAAR Verification | `/dashboard/verify-apaar/` | Yes |
| Logout | `/logout/` | Yes |
| Admin Panel | `/admin/` | Superuser |

---

## API Endpoints

### Test with cURL or Postman

#### Verify APAAR ID
```powershell
curl -X POST http://localhost:8000/api/verify-apaar/ `
  -H "Content-Type: application/json" `
  -d '{
    "apaar_id": "APAAR123",
    "name": "Test User",
    "income": 5000,
    "education_level": "High School",
    "location": "Delhi, India"
  }'
```

#### Apply as Beneficiary
```powershell
curl -X POST http://localhost:8000/api/apply/ `
  -H "Content-Type: application/json" `
  -d '{
    "apaar_id": "TEST123",
    "phone": "9876543210",
    "name": "John Doe"
  }'
```

---

## Troubleshooting

### Issue: "Template Not Found"
**Solution**: Ensure you're in the correct directory with `frontend/` folder

### Issue: "Static files not loading"
**Solution**: 
```powershell
python manage.py collectstatic --noinput
```

### Issue: "Database locked"
**Solution**: 
```powershell
# Close all terminals running the server
# Restart the server
python manage.py runserver
```

### Issue: "Port already in use"
**Solution**: 
```powershell
# Use a different port
python manage.py runserver 8001
```

---

## Project Files Modified/Created

### New Templates (in `frontend/`)
- ✅ `base.html` - Base template with navbar
- ✅ `home.html` - Landing page
- ✅ `signup.html` - Phone signup
- ✅ `verify_otp.html` - OTP verification
- ✅ `dashboard.html` - User dashboard
- ✅ `verify_apaar.html` - APAAR verification form

### Updated Files
- ✅ `frontend/static/css/style.css` - Complete styling
- ✅ `frontend/static/js/verify.js` - Form handler
- ✅ `saarthi2/settings.py` - Added accounts & dashboard apps
- ✅ `saarthi2/urls.py` - Complete URL routing
- ✅ `accounts/models.py` - UserProfile model
- ✅ `accounts/views.py` - Signup, OTP, logout views
- ✅ `accounts/admin.py` - Admin registration
- ✅ `dashboard/views.py` - Dashboard views
- ✅ `api/views.py` - Updated verification logic

### New Files
- ✅ `README.md` - Project documentation
- ✅ `SETUP.md` - This quick start guide
- ✅ Database migrations for accounts app

---

## Next Steps

1. **Customize Styling**: Edit `frontend/static/css/style.css`
2. **Add Features**: Extend models in respective apps
3. **Integrate Real APIs**: Replace mock functions with real integrations
4. **Deploy**: Follow Django deployment best practices

---

## Support

For issues or questions:
1. Check the main README.md
2. Review Django documentation
3. Check browser console for JavaScript errors
4. Review Django logs in terminal

---

**Happy Coding! 🚀**
