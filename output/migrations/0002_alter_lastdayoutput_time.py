# Generated by Django 4.2.11 on 2024-04-07 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('output', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastdayoutput',
            name='time',
            field=models.DateField(null=True),
        ),
    ]
