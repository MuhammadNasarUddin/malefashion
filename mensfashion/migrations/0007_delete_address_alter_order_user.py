# Generated by Django 5.0 on 2024-01-02 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensfashion', '0006_address'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mensfashion.user'),
        ),
    ]