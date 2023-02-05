# Generated by Django 4.1.4 on 2023-02-03 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('department', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Job_title',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reports.department')),
            ],
        ),
        migrations.CreateModel(
            name='Task_type',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50, null=True)),
                ('job_title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.job_title')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=50)),
                ('description', models.TextField(null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reports.employee')),
                ('task_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reports.task_type')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='job_title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reports.job_title'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
