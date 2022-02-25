# Generated by Django 4.0.2 on 2022-02-24 14:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=16)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Assignee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ManipulationDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('manipulationdates_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crm_api.manipulationdates')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{8,15}$')])),
                ('mobile', models.CharField(blank=True, max_length=16, unique=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{8,15}$')])),
                ('company_name', models.CharField(max_length=100)),
                ('job', models.CharField(max_length=100)),
            ],
            bases=('crm_api.manipulationdates',),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('manipulationdates_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crm_api.manipulationdates')),
                ('is_signed', models.BooleanField()),
                ('amount', models.FloatField()),
                ('payment_due', models.DateTimeField()),
                ('client_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_api.client')),
            ],
            bases=('crm_api.manipulationdates',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('manipulationdates_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crm_api.manipulationdates')),
                ('attendees', models.IntegerField()),
                ('event_date', models.DateTimeField()),
                ('notes', models.TextField()),
                ('event_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_api.contract')),
            ],
            bases=('crm_api.manipulationdates',),
        ),
        migrations.CreateModel(
            name='EventAssignation',
            fields=[
                ('assignee_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crm_api.assignee')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='crm_api.event')),
            ],
            bases=('crm_api.assignee',),
        ),
        migrations.CreateModel(
            name='ContractAssignation',
            fields=[
                ('assignee_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crm_api.assignee')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='crm_api.contract')),
            ],
            bases=('crm_api.assignee',),
        ),
        migrations.CreateModel(
            name='ClientAssignation',
            fields=[
                ('assignee_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crm_api.assignee')),
                ('is_converted', models.BooleanField()),
                ('medium', models.CharField(max_length=100)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='crm_api.client')),
            ],
            bases=('crm_api.assignee',),
        ),
    ]