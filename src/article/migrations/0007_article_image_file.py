# Generated by Django 2.2.2 on 2019-07-21 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20190720_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image_file',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
