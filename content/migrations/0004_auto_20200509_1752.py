# Generated by Django 3.0.4 on 2020-05-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20200509_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
