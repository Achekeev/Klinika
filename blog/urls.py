from django.urls import path, include
from .views import ValidateOTP, ValidatePhoneSendOTP, \
    ValidatePhoneForgot, ForgotValidateOTP, RegisterView, UserAPI, \
    ForgetPasswordChange, LoginAPI, UserProfileChangeAPIView
from knox import views as knox_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('validate/', ValidatePhoneSendOTP.as_view()),
    path('verify/', ValidateOTP.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('profile/<int:pk>/', UserAPI.as_view()),
    path('profile/', UserAPI.as_view()),
    path('update-profile/<int:pk>/', UserProfileChangeAPIView.as_view()),
    path('reset-otp/', ValidatePhoneForgot.as_view()),
    path('reset-otp/verify/', ForgotValidateOTP.as_view()),
    path('pass-change/', ForgetPasswordChange.as_view()),
]