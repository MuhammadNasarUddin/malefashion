# Generated by Django 5.0 on 2024-01-08 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensfashion', '0014_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=100)),
            ],
        ),
    ]
