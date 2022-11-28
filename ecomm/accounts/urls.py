from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('login_1/',LoginView.as_view(),name='login'),
    path('user_logout/',login_required(LogoutView.as_view()), name='user_logout'),
    path('register/',SignUpView.as_view(),name='register'),
    path('contactus/',ContactUs.as_view(), name='contactus'),

    path('change_password/<token>/',ResetPasswordView.as_view(),name='change_password'),
    path('new_password/',login_required(ChangePasswordView.as_view()),name='new_password'),
    path('Forget_Password/',ForgetPasswordView.as_view(),name='Forget_Password'),

    path('userprofilepage/',UserProfilView.as_view(), name='userprofilepage'),
    path('adresses/',AddressView.as_view(), name='adresses'),
    path("addresses/edit/<slug:pk>/", edit_address.as_view(), name="edit_address"),
    path("addresses/delete/<slug:pk>/",delete_address.as_view(), name="delete_address"),
    path("addresses/set_default/<slug:pk>/",set_default.as_view(), name="set_default"),

    path('singleblog/',TemplateView.as_view(template_name='accounts/singleblog.html'), name='singleblog'),
    path('bloglist/',TemplateView.as_view(template_name='accounts/bloglist.html'), name='bloglist'),
    path('reset/',TemplateView.as_view(template_name='accounts/Reset_conf.html'), name='reset'),
    path('shop/',TemplateView.as_view(template_name='accounts/shop.html'), name='shop'),
    
    path('activate_email/<email_token>/', activate_email.as_view(), name="activate_email"),  

]


