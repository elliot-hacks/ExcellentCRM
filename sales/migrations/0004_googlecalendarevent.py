# Generated by Django 5.1.6 on 2025-02-19 05:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('sales', '0003_visitorinfos_last_visited'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCalendarEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('meeting_link', models.URLField(blank=True, null=True)),
                ('calendar_event_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
    ]
