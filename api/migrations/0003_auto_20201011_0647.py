# Generated by Django 3.1.1 on 2020-10-11 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201011_0630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prize',
            old_name='img',
            new_name='image',
        ),
    ]