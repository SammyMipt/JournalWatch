# Generated by Django 2.2.2 on 2019-08-18 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0014_auto_20190818_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]