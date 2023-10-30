# Generated by Django 4.2.5 on 2023-09-29 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_user_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='COUNTER',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.IntegerField(default=0)),
                ('category', models.CharField(default=None, max_length=50, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]