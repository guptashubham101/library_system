# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fandb', '0002_auto_20161011_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookissued',
            old_name='libraryAdmin',
            new_name='library_admin',
        ),
    ]
