from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('apply/', views.apply_beneficiary),
    path('upload-doc/', views.upload_document),
    path('verify-apaar/', views.verify_apaar),
    path('trigger-score/', views.trigger_manual_score),
    path('dashboard/', views.admin_dashboard),
    path('batch-sync/', views.batch_sync),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
