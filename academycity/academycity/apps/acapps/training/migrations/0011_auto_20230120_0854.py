# Generated by Django 3.1.13 on 2023-01-20 06:54

import academycity.apps.core.sql
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('training', '0010_auto_20230112_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compliances',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.SmallIntegerField(default=0)),
                ('file', models.FileField(upload_to='training/compliances/files')),
                ('extra_done', models.TextField(blank=True, null=True)),
                ('not_done', models.TextField(blank=True, null=True)),
                ('conclusion', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'compliance',
                'verbose_name_plural': 'compliances',
                'ordering': ['week'],
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
                'ordering': ['course_name'],
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Instructors',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='training_user_instructors', serialize=False, to='auth.user')),
                ('first_name', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('training_web', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='training_web_instructors', to='training.trainingweb')),
            ],
            options={
                'verbose_name': 'instructor',
                'verbose_name_plural': 'instructors',
                'ordering': ['last_name'],
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Platoons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platoon_number', models.SmallIntegerField(default=1)),
                ('platon_name', models.CharField(blank=True, default='', max_length=50, null=True)),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.PositiveSmallIntegerField(default=0)),
                ('grade', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'test',
                'verbose_name_plural': 'tests',
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TestsStructures',
            fields=[
                ('battalion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='battalion_testsstructures', serialize=False, to='training.battalions')),
                ('tests_structures_content', models.JSONField(null=True)),
                ('training_web', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='training_web_tests', to='training.trainingweb')),
            ],
            options={
                'verbose_name': 'test',
                'verbose_name_plural': 'tests',
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='sections',
            name='company',
        ),
        migrations.RemoveField(
            model_name='sections',
            name='training_web',
        ),
        migrations.RenameField(
            model_name='soldiers',
            old_name='discipline',
            new_name='position',
        ),
        migrations.RenameField(
            model_name='soldiers',
            old_name='user_id',
            new_name='userid',
        ),
        migrations.RemoveField(
            model_name='soldiers',
            name='squad',
        ),
        migrations.RemoveField(
            model_name='soldiers',
            name='strength',
        ),
        migrations.RemoveField(
            model_name='squads',
            name='section',
        ),
        migrations.AddField(
            model_name='companys',
            name='company_number',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='soldiers',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='training/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='soldiers',
            name='is_confirmed',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='soldiers',
            name='zip',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='Officer',
        ),
        migrations.DeleteModel(
            name='Sections',
        ),
        migrations.AddField(
            model_name='tests',
            name='soldier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='soldier_tests', to='training.soldiers'),
        ),
        migrations.AddField(
            model_name='platoons',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='company_platoons', to='training.companys'),
        ),
        migrations.AddField(
            model_name='platoons',
            name='instructor',
            field=models.ManyToManyField(default=1, related_name='instructor_platoons', to='training.Instructors'),
        ),
        migrations.AddField(
            model_name='platoons',
            name='training_web',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='training_web_platoons', to='training.trainingweb'),
        ),
        migrations.AddField(
            model_name='courses',
            name='instructor',
            field=models.ManyToManyField(default=1, related_name='instructor_courses', to='training.Instructors'),
        ),
        migrations.AddField(
            model_name='courses',
            name='training_web',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='training_web_courses', to='training.trainingweb'),
        ),
        migrations.AddField(
            model_name='compliances',
            name='platoon',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='platoon_compliences', to='training.platoons'),
        ),
        migrations.AddField(
            model_name='battalions',
            name='instructor',
            field=models.ManyToManyField(default=1, related_name='instructor_battalions', to='training.Instructors'),
        ),
        migrations.AddField(
            model_name='companys',
            name='instructor',
            field=models.ManyToManyField(default=1, related_name='instructor_companys', to='training.Instructors'),
        ),
        migrations.AddField(
            model_name='soldiers',
            name='course',
            field=models.ManyToManyField(default=1, related_name='course_soldiers', to='training.Courses'),
        ),
        migrations.AddField(
            model_name='soldiers',
            name='platoon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='platoon_soldiers', to='training.platoons'),
        ),
        migrations.AddField(
            model_name='squads',
            name='platoon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='platoon_squads', to='training.platoons'),
        ),
    ]