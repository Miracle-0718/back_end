# Generated by Django 4.2 on 2023-05-04 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guwen", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
