# Generated by Django 2.2.2 on 2019-08-18 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_auto_20190816_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='image_file',
        ),
        migrations.RemoveField(
            model_name='article',
            name='image_url',
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
