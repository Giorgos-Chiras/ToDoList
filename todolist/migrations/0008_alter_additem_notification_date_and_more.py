# Generated by Django 5.1.3 on 2024-12-31 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0007_additem_notification_date_additem_notification_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additem',
            name='notification_date',
            field=models.DateField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='additem',
            name='notification_time',
            field=models.TimeField(blank=True, default=None),
        ),
    ]