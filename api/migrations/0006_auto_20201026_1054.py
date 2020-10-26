# Generated by Django 3.1.1 on 2020-10-26 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20201026_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='incentives',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prize',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prizes', to='api.timeline'),
        ),
    ]
