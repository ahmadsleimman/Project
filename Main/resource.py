from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget
from .models import Student, Teacher, Inbox


class StudentResource(resources.ModelResource):
    renamed_user__username = Field(attribute='user__username', column_name='Username')
    renamed_user__email = Field(attribute='user__email', column_name='Email')
    renamed_name = Field(attribute='name', column_name='Student Name')
    renamed_track = Field(attribute='track', column_name='Track')
    renamed_created = Field(attribute='created', column_name='Created At', widget=DateWidget(format='%d/%m/%Y'))

    class Meta:
        model = Student
        fields = (
            'renamed_user__username', 'renamed_user__email', 'renamed_name', 'renamed_track', 'renamed_created'
        )


class TeacherResource(resources.ModelResource):
    renamed_user__username = Field(attribute='user__username', column_name='Username')
    renamed_user__email = Field(attribute='user__email', column_name='Email')
    renamed_name = Field(attribute='name', column_name='Teacher Name')
    renamed_created = Field(attribute='created', column_name='Created At', widget=DateWidget(format='%d/%m/%Y'))

    class Meta:
        model = Teacher
        fields = (
            'renamed_user__username', 'renamed_user__email', 'renamed_name', 'renamed_created'
        )


class InboxResource(resources.ModelResource):
    renamed_name = Field(attribute='name', column_name='Name')
    renamed_email = Field(attribute='email', column_name='Email')
    renamed_subject = Field(attribute='subject', column_name='Subject')
    renamed_message = Field(attribute='message', column_name='Message')
    renamed_isFeedback = Field(attribute='isFeedback', column_name='Feedback?')
    renamed_created = Field(attribute='created', column_name='Created At', widget=DateWidget(format='%d/%m/%Y'))

    class Meta:
        model = Inbox
        fields = (
            'renamed_name', 'renamed_email', 'renamed_subject', 'renamed_message', 'renamed_isFeedback',
            'renamed_created'
        )
