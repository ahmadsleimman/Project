from django.db import models
from django.contrib.auth.models import User
from Main.models import Student, Teacher

# Create your models here.
TRACK = (
    ('Web Development', 'Web Development'),
    ('Mobile Application', 'Mobile Application'),
    ('AI', 'AI'),
    ('Game Development', 'Game Development'),
    ('Desktop Application', 'Desktop Application'),
    ('Cyber Security', 'Cyber Security'),
)

LANGUAGE = (
    ('French', 'French'),
    ('English', 'English'),
    ('Arabic','Arabic')
)


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name='Course')
    track = models.CharField(choices=TRACK, max_length=20, verbose_name='Track')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.track}"

    class Meta:
        ordering = ['-created']
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        db_table = 'Course'


class Class(models.Model):
    name = models.CharField(max_length=30, verbose_name='Class Name')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Teacher")
    students = models.ManyToManyField(Student, blank=True, verbose_name="Students")
    nbr_students = models.PositiveIntegerField(verbose_name="Max number of Students")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course")
    language = models.CharField(choices=LANGUAGE, max_length=10, verbose_name='Language')
    price = models.FloatField(verbose_name='Price')
    img_class = models.ImageField(verbose_name="Image", upload_to="photo/")
    classroom_link = models.CharField(max_length=255, verbose_name='Classroom Link')
    zoom_link = models.CharField(max_length=255, verbose_name='Zoom Link')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.language}"

    class Meta:
        ordering = ['-created']
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        db_table = 'Class'


class ClassRequest(models.Model):
    myclass = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="Class")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Student")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Class Request"
        verbose_name_plural = " Class Requests"
        db_table = 'Class_Request'

    def __str__(self):
        return f"{self.id}"


class ClassMessage(models.Model):
    myclass = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="Class")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    body = models.TextField(verbose_name='Body', null=True, blank=True)
    voice = models.FileField(verbose_name="Voice", upload_to="voice/%y/%m/%d", null=True, blank=True)
    image = models.ImageField(verbose_name="Image", upload_to="image/%y/%m/%d", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        verbose_name = "Class Message"
        verbose_name_plural = "Class Messages"
        db_table = 'Class_Message'

    def __str__(self):
        return f"{self.id}"


class ClassFinancialAid(models.Model):
    myclass = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="Class")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Student")
    message = models.TextField(verbose_name='Message')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Class Financial Aid"
        verbose_name_plural = "Class Financial Aids"
        db_table = 'Class_Financial_Aid'

    def __str__(self):
        return f"{self.id}"
