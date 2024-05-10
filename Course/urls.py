from django.urls import path
from .views import Classes, ClassDetails, ClassEnroll, ClassFinancialAidEnroll

urlpatterns = [
    path('classes', Classes, name='Classes'),
    path('classes/<str:id>', ClassDetails, name='ClassDetails'),
    path('classes/<str:id>/enroll', ClassEnroll, name='ClassEnroll'),
    path('classes/<str:id>/financial-aid', ClassFinancialAidEnroll, name='ClassFinancialAid'),
]
