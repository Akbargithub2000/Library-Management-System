# Generated by Django 4.1.1 on 2023-09-23 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_members_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['bookId']},
        ),
        migrations.RenameField(
            model_name='book',
            old_name='bookID',
            new_name='bookId',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='language_code',
            new_name='language',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='publication_on_date',
            new_name='publication_date',
        ),
    ]
