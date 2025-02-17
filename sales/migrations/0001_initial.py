# Generated by Django 5.1.6 on 2025-02-17 13:49

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField()),
            ],
            options={
                'verbose_name': 'ContactMessage',
                'verbose_name_plural': 'ContactMessages',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(help_text='Enter the email subject.', max_length=255)),
                ('message', models.TextField(help_text='Enter the email message.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'EmailTemplate',
                'verbose_name_plural': 'EmailTemplates',
            },
        ),
        migrations.CreateModel(
            name='EmailTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('opened_at', models.DateTimeField(blank=True, null=True)),
                ('clicked_link', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('email_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.emailtemplate')),
            ],
        ),
        migrations.CreateModel(
            name='VisitorInfos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('referrer', models.URLField(blank=True, null=True)),
                ('page_visited', models.TextField()),
                ('action', models.TextField(blank=True, null=True)),
                ('visit_count', models.PositiveIntegerField(default=1)),
                ('event_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('region', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('isp', models.CharField(blank=True, max_length=255, null=True)),
                ('timezone', models.CharField(blank=True, max_length=255, null=True)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'VisitorInfo',
                'verbose_name_plural': 'VisitorInfos',
            },
        ),
    ]
