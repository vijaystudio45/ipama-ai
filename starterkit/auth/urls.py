from django.urls import path
from django.conf import settings
from auth.signin.views import AuthSigninView,logout_req,AuthverificationView
from auth.signup.views import AuthSignupView
from auth.reset_password.views import AuthResetPasswordView
from auth.new_password.views import AuthNewPasswordView

app_name = 'auth'

urlpatterns = [
    path('signin', AuthSigninView.as_view(template_name = 'pages/auth/signin.html'), name='signin'),
    path('signup', AuthSignupView.as_view(template_name = 'pages/auth/signup.html'), name='signup'),
    path('reset-password', AuthResetPasswordView.as_view(template_name = 'pages/auth/reset-password.html'), name='reset-password'),
    path('new-password', AuthNewPasswordView.as_view(template_name = 'pages/auth/new-password.html'), name='new-password'),

    path('password_reset/confirm/<str:user_id>/', AuthNewPasswordView.as_view(template_name = 'pages/auth/new-password.html'), name='password_reset_confirm'),
    path('logout', logout_req, name='logout'),
    path('verification/', AuthverificationView.as_view(template_name = 'pages/auth/verification.html'), name='verification'),

]