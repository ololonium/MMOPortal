# Generated by Django 4.2.7 on 2023-11-18 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsboard', '0007_alter_comment_comment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]