from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import redirect, reverse
from allauth.account.signals import user_logged_in
from .models import Student


@receiver(user_logged_in)
def addStudent(request, user, **kwargs):
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        Student.objects.create(user=user, name=user)

# user_logged_in.connect(receiver=addStudent, sender=User)
