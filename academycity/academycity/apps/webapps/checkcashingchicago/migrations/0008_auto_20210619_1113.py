# Generated by Django 3.1.11 on 2021-06-19 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkcashingchicago', '0007_auto_20210619_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkcashingweb',
            name='partner_title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, default=1000)),
                ('partner_image', models.ImageField(blank=True, null=True, upload_to='partner/')),
                ('partner_description', models.CharField(max_length=100, null=True)),
                ('image_id', models.IntegerField(default=0)),
                ('image_width', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('check_cashing_web', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='checkcashingchicago.checkcashingweb')),
            ],
            options={
                'verbose_name': 'partner',
                'verbose_name_plural': 'partners',
                'ordering': ['order'],
            },
        ),
    ]