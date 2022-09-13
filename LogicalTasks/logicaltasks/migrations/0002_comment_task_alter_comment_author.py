# Generated by Django 4.0.4 on 2022-09-12 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('logicaltasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='logicaltasks.task'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
