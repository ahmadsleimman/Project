from django.contrib import admin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Course, Class, ClassRequest, ClassMessage, ClassFinancialAid
from Main.models import Student
from import_export.admin import ImportExportModelAdmin
from .resource import CourseResource, ClassResource


# Register your models here.

class ClassInline(admin.TabularInline):
    model = Class
    extra = 0
    readonly_fields = ['name', 'course']
    fields = ['name', 'course']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'track', 'created')
    search_fields = ('id', 'name')
    list_filter = ('track',)
    list_per_page = 20
    resource_class = CourseResource

    def has_import_permission(self, request):
        # Only superusers have export permission
        return request.user.is_superuser

    def has_export_permission(self, request):
        # Only superusers have export permission
        return request.user.is_superuser


@admin.register(Class)
class ClassAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'teacher_name', 'course_name', 'course_track', 'language', 'price', 'created')
    search_fields = ('id', 'name', 'teacher__name', 'course__name')
    filter_horizontal = ('students',)
    list_filter = ('course__track', 'course__name', 'language')
    list_per_page = 30
    actions = ['sendNewClassEmail', 'deleteAllMessage']
    resource_class = ClassResource

    @admin.display(description="Teacher", ordering="teacher__name")
    def teacher_name(self, obj):
        return obj.teacher.name

    @admin.display(description="Course", ordering="course__name")
    def course_name(self, obj):
        return obj.course.name

    @admin.display(description="Track", ordering="course__track")
    def course_track(self, obj):
        return obj.course.track

    def sendNewClassEmail(self, request, queryset):
        for obj in queryset:
            students = Student.objects.filter(track=obj.course.track)
            for student in students:
                if student.user.email is not None:
                    email = student.user.email
                    subject = "New Class is Open - Academy Tech Learn"
                    message = render_to_string('email/new_class_email.html', {
                        'student': student.name,
                        'price': obj.price,
                        'teacher': obj.teacher.name,
                        'className': obj.name,
                        'courseName': obj.course.name,
                    })
                    email = EmailMessage(subject=subject, body=message, to=[email])
                    email.send()

    sendNewClassEmail.short_description = 'Send Notification Email For New Class'

    def deleteAllMessage(self, request, queryset):
        for obj in queryset:
            myclass = Class.objects.get(id=obj.id)
            ClassMessage.objects.filter(myclass=myclass).delete()

    deleteAllMessage.short_description = 'Delete All Messages'

    def has_import_permission(self, request):
        return False

    def has_export_permission(self, request):
        # Only superusers have export permission
        return request.user.is_superuser


@admin.register(ClassRequest)
class ClassRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'student_name', 'class_id', 'class_name', 'created')
    list_per_page = 30
    search_fields = ('student__name',)
    list_filter = ('myclass__course__track',)

    @admin.display(description="Student ID")
    def student_id(self, obj):
        return obj.student.id

    @admin.display(description="Student Name", ordering="student__name")
    def student_name(self, obj):
        return obj.student.name

    @admin.display(description="Class ID", ordering="myclass__id")
    def class_id(self, obj):
        return obj.myclass.id

    @admin.display(description="Class Name", ordering="myclass__name")
    def class_name(self, obj):
        return obj.myclass.name

    def acceptStudent(self, request, queryset):
        for obj in queryset:
            if obj.student not in obj.myclass.students.all():
                obj.myclass.students.add(obj.student)
                email = obj.student.user.email
                subject = "Congratulations! You've Been Accepted into the " + obj.myclass.name
                message = render_to_string('email/accept_request_email.html', {
                    'student': obj.student.name,
                    'className': obj.myclass.name,
                    'courseName': obj.myclass.course.name,
                })
                email = EmailMessage(subject=subject, body=message, to=[email])
                email.send()
            obj.delete()

    acceptStudent.short_description = 'Accept Student'
    actions = [acceptStudent]


@admin.register(ClassMessage)
class ClassMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_username', 'class_name', 'created')
    search_fields = ('myclass__name', 'user__username', 'user__email')
    list_per_page = 30

    @admin.display(description="Username", ordering="user__username")
    def user_username(self, obj):
        return obj.user.username

    @admin.display(description="Class Name", ordering="myclass__name")
    def class_name(self, obj):
        return obj.myclass.name


@admin.register(ClassFinancialAid)
class ClassFinancialAidAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'student_name', 'class_id', 'class_name', 'created')
    list_per_page = 20
    search_fields = ('student__name', 'myclass__name')

    @admin.display(description="Student ID", ordering="student__id")
    def student_id(self, obj):
        return obj.student.id

    @admin.display(description="Student Name", ordering="student__name")
    def student_name(self, obj):
        return obj.student.name

    @admin.display(description="Class ID", ordering="myclass__id")
    def class_id(self, obj):
        return obj.myclass.id

    @admin.display(description="Class Name", ordering="myclass__name")
    def class_name(self, obj):
        return obj.myclass.name
