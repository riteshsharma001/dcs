from django.urls import path
from .views import ChangePasswordView, ResetPasswordView, ResetPasswordConfirmView

urlpatterns = [
    path('password_change/', ChangePasswordView.as_view(), name = 'password_change'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset_confirm/', ResetPasswordConfirmView.as_view, name='password_reset_confirm'),

]