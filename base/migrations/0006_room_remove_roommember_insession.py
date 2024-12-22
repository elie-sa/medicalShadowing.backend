# Generated by Django 5.1.4 on 2024-12-22 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_roommember_room_name_delete_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('session_time', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='roommember',
            name='insession',
        ),
    ]
