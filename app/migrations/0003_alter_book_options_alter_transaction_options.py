# Generated by Django 4.1.1 on 2023-09-22 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_members_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['bookID']},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-issued_date']},
        ),
    ]