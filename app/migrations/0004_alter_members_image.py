# Generated by Django 4.1.1 on 2023-09-22 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_book_options_alter_transaction_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]