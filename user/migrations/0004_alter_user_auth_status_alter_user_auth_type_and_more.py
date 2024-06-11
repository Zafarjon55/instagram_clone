# Generated by Django 5.0.4 on 2024-04-29 05:39

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_status',
            field=models.CharField(choices=[('new', 'new'), ('code_verified', 'code_verified'), ('done', 'done'), ('photo_done', 'photo_done')], default='new', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='auth_type',
            field=models.CharField(choices=[('via_email', 'via_email'), ('via_phone', 'via_phone')], max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_roles',
            field=models.CharField(choices=[('ordinary_user', 'ordinary_user'), ('maneger', 'maneger'), ('admin', 'admin')], default='ordinary_user', max_length=100),
        ),
        migrations.AlterField(
            model_name='userconfirmation',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]