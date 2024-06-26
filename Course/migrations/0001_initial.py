# Generated by Django 5.0.3 on 2024-05-09 15:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Course')),
                ('track', models.CharField(choices=[('Web Development', 'Web Development'), ('Mobile Application', 'Mobile Application'), ('AI', 'AI'), ('Game Development', 'Game Development'), ('Desktop Application', 'Desktop Application'), ('Cyber Security', 'Cyber Security')], max_length=20, verbose_name='Track')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'db_table': 'Course',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Class Name')),
                ('nbr_students', models.PositiveIntegerField(verbose_name='Max number of Students')),
                ('language', models.CharField(choices=[('French', 'French'), ('English', 'English')], max_length=10, verbose_name='Language')),
                ('price', models.FloatField(verbose_name='Price')),
                ('img_class', models.ImageField(upload_to='photo/', verbose_name='Image')),
                ('classroom_link', models.CharField(max_length=255, verbose_name='Classroom Link')),
                ('zoom_link', models.CharField(max_length=255, verbose_name='Zoom Link')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('students', models.ManyToManyField(blank=True, to='Main.student', verbose_name='Students')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.teacher', verbose_name='Teacher')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.course', verbose_name='Course')),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
                'db_table': 'Class',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ClassFinancialAid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('myclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.class', verbose_name='Class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Class Financial Aid',
                'verbose_name_plural': 'Class Financial Aids',
                'db_table': 'Class_Financial_Aid',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ClassMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Body')),
                ('voice', models.FileField(blank=True, null=True, upload_to='voice/%y/%m/%d', verbose_name='Voice')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/%y/%m/%d', verbose_name='Image')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('myclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.class', verbose_name='Class')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Class Message',
                'verbose_name_plural': 'Class Messages',
                'db_table': 'Class_Message',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='ClassRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('myclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.class', verbose_name='Class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Class Request',
                'verbose_name_plural': ' Class Requests',
                'db_table': 'Class_Request',
                'ordering': ['-created'],
            },
        ),
    ]
