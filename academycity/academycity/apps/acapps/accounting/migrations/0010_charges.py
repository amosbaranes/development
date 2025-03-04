# Generated by Django 3.1.13 on 2022-05-31 12:51

import academycity.apps.core.sql
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_auto_20220531_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('amount', models.IntegerField(blank=True, default=0)),
                ('reason', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('accounting_web', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='accounting_charges', to='accounting.accountingweb')),
                ('student', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='student_charges', to='accounting.students')),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]
