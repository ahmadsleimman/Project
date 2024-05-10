from django.db import models
from django.contrib.auth.models import User

# Create your models here.


TRACK = (
    ('Web Development', 'Web Development'),
    ('Mobile Application', 'Mobile Application'),
    ('AI', 'AI'),
    ('Game Development', 'Game Development'),
    ('Desktop Application', 'Desktop Application'),
    ('Cyber Security', 'Cyber Security'),
    ('None', 'None'),
)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    name = models.CharField(max_length=40, verbose_name='Student Name')
    track = models.CharField(choices=TRACK, max_length=20, verbose_name='Track', default="None")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        ordering = ['-created']
        verbose_name = "Student"
        verbose_name_plural = "Students"
        db_table = 'Student'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    name = models.CharField(max_length=40, verbose_name='Teacher Name')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        ordering = ['-created']
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        db_table = 'Teacher'


class Inbox(models.Model):
    name = models.CharField(max_length=45, verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=45, verbose_name='Subject')
    message = models.TextField(verbose_name='Message')
    isFeedback = models.BooleanField(verbose_name='Is Feedback', default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Inbox"
        verbose_name_plural = "Inboxes"
        db_table = 'Inbox'

    def __str__(self):
        return f"{self.id}"
