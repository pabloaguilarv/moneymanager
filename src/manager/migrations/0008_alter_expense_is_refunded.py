# Generated by Django 4.0.4 on 2022-08-07 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_alter_settings_end_date_alter_settings_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='is_refunded',
            field=models.CharField(blank=True, default='refunded?', max_length=200, null=True),
        ),
    ]
