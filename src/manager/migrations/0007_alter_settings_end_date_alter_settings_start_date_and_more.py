# Generated by Django 4.0.4 on 2022-08-06 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_alter_settings_end_date_alter_settings_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='settings',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.DeleteModel(
            name='SettingsUpdateView',
        ),
    ]
