# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fandb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='createdOn',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='isActive',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='sessionId',
            new_name='session_id',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='updatedOn',
            new_name='updated_on',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='userId',
            new_name='user_id',
        ),
        migrations.RemoveField(
            model_name='libraryadmin',
            name='adminId',
        ),
        migrations.AddField(
            model_name='libraryadmin',
            name='admin_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
