# Generated by Django 5.1.7 on 2025-03-13 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WimHofSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_global', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BreathingRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.PositiveIntegerField()),
                ('breath_count', models.PositiveIntegerField(help_text='Number of breaths in this round')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='wimhof.wimhofsession')),
            ],
            options={
                'ordering': ['round_number'],
            },
        ),
        migrations.CreateModel(
            name='WimHofStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('round_data', models.JSONField(default=dict, help_text='JSON data with round stats')),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wimhof.wimhofsession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
