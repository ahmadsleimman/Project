from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget, ManyToManyWidget
from .models import Course, Class
from Main.models import Student


class CourseResource(resources.ModelResource):
    renamed_name = Field(attribute='name', column_name='Course Name')
    renamed_track = Field(attribute='track', column_name='Track')
    renamed_created = Field(attribute='created', column_name='Created At', widget=DateWidget(format='%d/%m/%Y'))

    class Meta:
        model = Course
        fields = (
            'renamed_name', 'renamed_track', 'renamed_created'
        )


class ClassResource(resources.ModelResource):
    renamed_name = Field(attribute='name', column_name='Class Name')
    renamed_teacher__name = Field(attribute='teacher__name', column_name='Teacher Name')
    renamed_students = Field(attribute='students', column_name='Students',
                             widget=ManyToManyWidget(Student, field='name', separator='|'))
    renamed_course__name = Field(attribute='course__name', column_name='Course Name')
    renamed_course__track = Field(attribute='course__track', column_name='Course Track')
    renamed_language = Field(attribute='language', column_name='Language')
    renamed_price = Field(attribute='price', column_name='Price')
    renamed_classroom_link = Field(attribute='classroom_link', column_name='Classroom Link')
    renamed_zoom_link = Field(attribute='zoom_link', column_name='Zoom Link')
    renamed_created = Field(attribute='created', column_name='Created At', widget=DateWidget(format='%d/%m/%Y'))

    class Meta:
        model = Class
        fields = (
            'renamed_name', 'renamed_teacher__name', 'renamed_students', 'renamed_course__name',
            'renamed_course__track', 'renamed_language', 'renamed_price', 'renamed_classroom_link',
            'renamed_zoom_link', 'renamed_created'
        )
