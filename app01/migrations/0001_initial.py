# Generated by Django 3.1.4 on 2020-12-13 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('departmentId', models.AutoField(primary_key=True, serialize=False)),
                ('departmentName', models.CharField(max_length=255)),
                ('departmentPwd', models.CharField(max_length=255)),
                ('organizationId', models.IntegerField()),
            ],
        ),
    ]
