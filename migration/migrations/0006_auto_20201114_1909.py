# Generated by Django 3.0 on 2020-11-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('migration', '0005_auto_20201114_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categoryName',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tagName',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
