# Generated by Django 3.1.13 on 2022-12-06 06:35

import academycity.apps.core.sql
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneDim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene_code', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PersonDim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_code', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=16, null=True)),
                ('gene_dim', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='gene_dim_fact', to='ms.genedim')),
                ('person_dim', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='person_dim_fact', to='ms.persondim')),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]