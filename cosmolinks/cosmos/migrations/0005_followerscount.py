# Generated by Django 4.2.2 on 2023-08-15 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmos', '0004_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]