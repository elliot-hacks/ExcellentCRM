# Generated by Django 5.1.6 on 2025-02-15 09:53

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visitorinfos',
            options={},
        ),
        migrations.AddField(
            model_name='visitorinfos',
            name='action',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visitorinfos',
            name='referrer',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visitorinfos',
            name='session_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='visitorinfos',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visitorinfos',
            name='user_agent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='visitorinfos',
            name='event_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='visitorinfos',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='visitorinfos',
            name='page_visited',
            field=models.TextField(),
        ),
    ]
