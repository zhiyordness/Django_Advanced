from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('fbv/login/', views.login_fbv, name='login-fbv'),
    path('fbv/logout/', views.logout_fbv, name='logout-fbv'),
    path('fbv/register/', views.register_fbv, name='register-fbv'),
    path('cbv/login/', LoginView.as_view(template_name='accounts/login.html'), name='login-cbv'),
    path('cbv/logout/', LogoutView.as_view(), name='logout-cbv'),
    path('cbv/register/', views.RegisterView.as_view(), name='register-cbv'),
    path('details/', views.ProfileDetailView.as_view(), name='detail'),
    path('set-unusable-password/', views.set_unusable_password, name='set-unusable-password'),
    path('password-change/', PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url=reverse_lazy('accounts:password_change_done')
    ), name='change_password'),
    path('password-change-done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),

    # FIXED: Added success_url with namespace
    path('password-reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_subject_reset_email.txt',
        success_url=reverse_lazy('accounts:password_reset_done'),
        from_email = 'noreply@yourdomain.com'
# Added this line
    ), name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
    ), name='password_reset_done'),

    # FIXED: Fixed the URL pattern to include token parameter
    path('password-reset/confirm/<uidb64>/<token>',  # Added <token>/ to the URL
         PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete')
         ), name='password_reset_confirm'),

    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]