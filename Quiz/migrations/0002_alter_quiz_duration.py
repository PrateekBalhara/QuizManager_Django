# Generated by Django 4.0.4 on 2022-04-22 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='duration',
            field=models.IntegerField(),
        ),
    ]
