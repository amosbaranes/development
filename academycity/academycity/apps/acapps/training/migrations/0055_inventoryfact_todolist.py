# Generated by Django 3.1.13 on 2023-05-23 11:29

import academycity.apps.core.sql
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0054_soldierqualificationfact'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('subject', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=1000)),
                ('priority', models.PositiveSmallIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_todolists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'todolist',
                'verbose_name_plural': 'todolist',
                'ordering': ['-is_active', '-priority'],
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='InventoryFact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('inventory', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='inventory_inventory_facts', to='training.inventorys')),
                ('soldier', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='soldier_inventory_facts', to='training.soldiers')),
            ],
            options={
                'verbose_name': 'grades_for_event',
                'verbose_name_plural': 'grades_for_events',
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]