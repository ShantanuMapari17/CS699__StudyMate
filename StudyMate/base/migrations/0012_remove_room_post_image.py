# Generated by Django 4.1.2 on 2022-11-04 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0011_alter_room_post_image"),
    ]

    operations = [
        migrations.RemoveField(model_name="room", name="post_image",),
    ]
