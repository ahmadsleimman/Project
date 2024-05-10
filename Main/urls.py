from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import Home, About, ContactUs, Service, NotFound, loginUser, registerUser, logout, verify_email, MyClasses, \
    CompleteAccount, Profile, verify_message

urlpatterns = [
    path('', Home, name='Home'),

    path('login', loginUser, name='Login'),

    path('register', registerUser, name='Register'),

    path('verify-account', verify_message, name='verify_message'),

    path('logout', logout, name='Logout'),

    path('about', About, name='About'),

    path('service', Service, name='Service'),

    path('contact-us', ContactUs, name='Contact'),

    path('myclasses', MyClasses, name='MyClasses'),

    path('profile', Profile, name='Profile'),

    path('404', NotFound, name='NotFound'),

    path('complete-account/', CompleteAccount, name='CompleteAccount'),

    path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name='email/reset_password_email.html',
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('Login')
    ), name='password_reset_confirm'),
]
