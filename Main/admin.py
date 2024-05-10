from django.contrib import admin
from .models import Student, Teacher, Inbox
from Course.admin import ClassInline
from import_export.admin import ImportExportModelAdmin
from .resource import StudentResource, TeacherResource, InboxResource


# Register your models here.


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'email', 'username', 'track', 'created')
    search_fields = ('id', 'name')
    list_filter = ('track',)
    list_per_page = 30
    resource_class = StudentResource

    @admin.display(description="Email", ordering="user__email")
    def email(self, obj):
        return obj.user.email

    @admin.display(description="Username", ordering="user__username")
    def username(self, obj):
        return obj.user.username

    def has_import_permission(self, request):
        return False

    def has_export_permission(self, request):
        # Only superusers have export permission
        return request.user.is_superuser


@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'email', 'username', 'created')
    search_fields = ('id', 'name')
    inlines = [ClassInline]
    resource_class = TeacherResource

    @admin.display(description="Email", ordering="user__email")
    def email(self, obj):
        return obj.user.email

    @admin.display(description="Username", ordering="user__username")
    def username(self, obj):
        return obj.user.username

    def has_import_permission(self, request):
        return False

    def has_export_permission(self, request):
        # Only superusers have export permission
        return request.user.is_superuser


@admin.register(Inbox)
class InboxAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'message', 'isFeedback', 'created')
    search_fields = ('id', 'name', 'subject', 'email')
    list_filter = ('isFeedback',)
    list_per_page = 20
    resource_class = InboxResource

    def has_import_permission(self, request):
        return False

    def has_export_permission(self, request):
        # Only superusers have export permission
        return request.user.is_superuser
