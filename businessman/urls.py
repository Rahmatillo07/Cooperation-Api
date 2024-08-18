from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import UserApiView, ChatApiView, RegisterApiView, LocationUpdateView, GoogleLoginView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/v1/users', UserApiView)
router.register('api/v1/chats', ChatApiView)

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/register/', RegisterApiView.as_view()),
    path('api/v1/update-location/', LocationUpdateView.as_view(), name='update-location'),
    path('api-auth/', include('rest_framework.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('social_django.urls', namespace='social')),

    path('api/v1/auth/google/', GoogleLoginView.as_view(), name='google-login'),
]
