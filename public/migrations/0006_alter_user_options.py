# Generated by Django 4.2.9 on 2024-03-26 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0005_alter_user_password_alter_user_role_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['name']},
        ),
    ]