# Generated by Django 4.1.2 on 2022-10-28 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0010_alter_room_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="post_image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
