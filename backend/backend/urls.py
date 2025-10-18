from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import register_user  # ✅ import the new register view

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Student API endpoints
    path('api/', include('api.urls')),  # e.g. /api/students/

    # ✅ JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ New registration endpoint
    path('api/register/', register_user, name='register_user'),
]
