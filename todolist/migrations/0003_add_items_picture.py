# Generated by Django 5.1.3 on 2024-11-09 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_add_items_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_items',
            name='picture',
            field=models.ImageField(blank=True, default='default.jpg', upload_to=''),
        ),
    ]