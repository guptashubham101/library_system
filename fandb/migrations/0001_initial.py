# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookIssued',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_submission', models.DateTimeField()),
                ('date_of_issue', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'book_issued',
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ISBN', models.IntegerField()),
                ('availability', models.BooleanField(default=False)),
                ('is_issued', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
            ],
            options={
                'db_table': 'books',
            },
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('days', models.IntegerField()),
            ],
            options={
                'db_table': 'fine',
            },
        ),
        migrations.CreateModel(
            name='LibraryAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('admin_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'library_admin',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_id', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField()),
                ('user_id', models.IntegerField()),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'session',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student_name', models.CharField(max_length=255)),
                ('student_roll_number', models.CharField(max_length=255)),
                ('student_email', models.CharField(max_length=255)),
                ('branch', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('semester', models.IntegerField()),
                ('year', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.AddField(
            model_name='fine',
            name='student',
            field=models.ForeignKey(to='fandb.Student'),
        ),
        migrations.AddField(
            model_name='bookissued',
            name='books',
            field=models.ForeignKey(to='fandb.Books'),
        ),
        migrations.AddField(
            model_name='bookissued',
            name='libraryAdmin',
            field=models.ForeignKey(to='fandb.LibraryAdmin'),
        ),
        migrations.AddField(
            model_name='bookissued',
            name='student',
            field=models.ForeignKey(to='fandb.Student'),
        ),
    ]
