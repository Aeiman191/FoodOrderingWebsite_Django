# Generated by Django 4.0.3 on 2022-03-29 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='phone',
            field=models.PositiveIntegerField(),
        ),
    ]
