# Generated by Django 4.2.4 on 2024-12-01 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('invite_code', models.CharField(max_length=6, unique=True)),
                ('activated_invite_code', models.CharField(blank=True, max_length=6, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('invited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invited_users', to='referrals.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
