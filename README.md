# SAARTHI Platform - Digital Verification System

## Overview
SAARTHI (Securing Authenticity & Accountability through Robust Technological Healthcare Integration) is a blockchain-backed digital verification platform that uses APAAR IDs, AI-powered trust scoring, and DigiLocker integration to ensure authentic, tamper-proof beneficiary verification.

## Project Structure

```
saarthi2/
├── frontend/                    # Frontend templates and static files
│   ├── base.html               # Base template with navbar and footer
│   ├── home.html               # Landing page
│   ├── signup.html             # Phone signup page
│   ├── verify_otp.html         # OTP verification page
│   ├── dashboard.html          # User dashboard
│   ├── verify_apaar.html       # APAAR verification form
│   └── static/
│       ├── css/
│       │   └── style.css       # Complete styling
│       └── js/
│           └── verify.js       # Verification form handler
│
├── saarthi2/                   # Django project
│   ├── accounts/               # User authentication app
│   │   ├── models.py           # UserProfile model
│   │   ├── views.py            # Signup, OTP, logout views
│   │   └── admin.py            # Admin registration
│   │
│   ├── dashboard/              # Dashboard app
│   │   ├── views.py            # Dashboard and verify views
│   │   └── models.py
│   │
│   ├── api/                    # API app
│   │   ├── models.py           # Beneficiary, VerificationRecord
│   │   ├── views.py            # API endpoints
│   │   ├── serializers.py      # DRF serializers
│   │   └── urls.py             # API routes
│   │
│   └── saarthi2/               # Main project settings
│       ├── settings.py         # Project configuration
│       ├── urls.py             # URL routing
│       └── wsgi.py
│
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Features

### 1. **Homepage / Landing Page** (`/`)
- Introduces SAARTHI platform
- Problem statement and solution overview
- Key features showcase
- Call-to-action buttons

### 2. **Signup Flow** (`/signup/` and `/verify-otp/`)
- Phone number-based signup
- OTP verification (hardcoded as `1234` for demo)
- Automatic user creation
- Session-based authentication

### 3. **User Dashboard** (`/dashboard/`)
- User information display
- Quick access to APAAR verification
- Verification history table
- Logout functionality

### 4. **APAAR Verification** (`/dashboard/verify-apaar/`)
- Form with fields: APAAR ID, name, income, education, location
- JavaScript-based form submission
- Real-time API response display
- Trust score calculation
- Status indicators (success/manual_review/failed)

## Technology Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite3 (development)
- **API**: Django REST Framework 3.16.1
- **Authentication**: Session-based (with JWT ready for future)
- **Frontend**: Django Templates (no React)
- **Styling**: Custom CSS with responsive design
- **JavaScript**: Vanilla JS (no frameworks)

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd saarthi2
   ```

2. **Create virtual environment**
   ```bash
   python -m venv env
   .\env\Scripts\activate  # Windows
   # source env/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   cd saarthi2
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Homepage: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## Usage Guide

### For Users

1. **Sign Up**
   - Go to http://localhost:8000/signup/
   - Enter a 10-digit phone number
   - Click "Send OTP"

2. **Verify OTP**
   - Enter OTP: `1234` (hardcoded for demo)
   - Click "Verify & Login"

3. **Access Dashboard**
   - View your user information
   - See verification history
   - Click "Verify APAAR ID"

4. **Verify APAAR ID**
   - Use demo IDs: `APAAR123` or `VALID123`
   - Fill in all required fields
   - Submit and view results
   - Trust score and status displayed

### Demo Credentials
- **OTP**: `1234`
- **Valid APAAR IDs**: `APAAR123`, `VALID123`

## API Endpoints

### Public Endpoints
- `POST /api/verify-apaar/` - Verify APAAR ID with user details
- `POST /api/apply/` - Register new beneficiary
- `POST /api/upload-document/` - Upload documents
- `POST /api/batch-sync/` - Batch sync offline applications

### Protected Endpoints (require authentication)
- `POST /api/trigger-manual-score/` - Re-run scoring with more data
- `GET /api/admin-dashboard/` - Admin statistics

## Database Models

### UserProfile (accounts app)
- `user` - OneToOne with Django User
- `phone` - Unique phone number
- `otp` - Temporary OTP storage
- `otp_verified` - Verification status

### Beneficiary (api app)
- `apaar_id` - Unique APAAR identifier
- `name` - Full name
- `phone` - Contact number
- `caste_certificate` - Certificate URL
- `state` - Location state
- `verified` - Verification status

### VerificationRecord (api app)
- `beneficiary` - ForeignKey to Beneficiary
- `raw_data` - JSON field for verification data
- `trust_score` - AI-calculated score (0-100)
- `status` - pending/success/manual_review/failed

### BlockchainHash (api app)
- `verification` - OneToOne with VerificationRecord
- `hash` - SHA256 hash of verification
- `created_at` - Timestamp

## Future Enhancements

### Phase 1 - Authentication
- [ ] Integrate real OTP service (Twilio/AWS SNS)
- [ ] Add password-based login option
- [ ] Implement forgot password flow

### Phase 2 - Verification
- [ ] Integrate DigiLocker API
- [ ] Connect to real APAAR database
- [ ] Implement document upload with file storage (S3)

### Phase 3 - AI/ML
- [ ] Build ML model for trust scoring
- [ ] Fraud detection patterns
- [ ] Anomaly detection

### Phase 4 - Blockchain
- [ ] Integrate with Ethereum/Hyperledger
- [ ] Store verification hashes on-chain
- [ ] Smart contracts for automated verification

### Phase 5 - Mobile App
- [ ] Offline-first mobile app for field agents
- [ ] Barcode/QR code scanning
- [ ] Batch sync capability

## Security Considerations

- **CSRF Protection**: Enabled on all forms
- **Session Security**: Secure session cookies
- **Input Validation**: Server-side validation on all inputs
- **SQL Injection**: Protected by Django ORM
- **XSS Protection**: Django's auto-escaping enabled

## Development Notes

- Templates are in `frontend/` folder (not separate templates directory)
- Static files served from `frontend/static/`
- CORS enabled for localhost:8000
- Debug mode ON (disable in production)
- Secret key should be changed in production

## Troubleshooting

### Common Issues

1. **Template Not Found**
   - Ensure `FRONTEND_DIR` is set correctly in settings.py
   - Check that templates are in the `frontend/` folder

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic` if needed
   - Check `STATICFILES_DIRS` in settings.py

3. **Database Errors**
   - Run migrations: `python manage.py migrate`
   - Delete `db.sqlite3` and re-migrate if needed

4. **Login Required Errors**
   - Ensure you're logged in via signup/OTP flow
   - Check session middleware is enabled

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is developed as part of a government initiative for welfare scheme verification.

## Contact

For questions or support, please contact the development team.

---

**Note**: This is a demo/prototype version. For production deployment, please ensure:
- Real OTP integration
- Secure secret key management
- HTTPS enabled
- Database optimization
- Proper error logging
- Rate limiting on APIs
- Data backup strategy
