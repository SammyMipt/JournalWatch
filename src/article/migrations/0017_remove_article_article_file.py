# Generated by Django 2.2.2 on 2019-08-18 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0016_auto_20190818_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='article_file',
        ),
    ]
