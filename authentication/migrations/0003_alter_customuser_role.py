# Generated by Django 5.1.6 on 2025-02-28 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_customuser_role_delete_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'Admin'), ('superadmin', 'Super Admin'), ('data_analyst', 'Data Analyst'), ('drone_controller', 'Drone Controller')], max_length=20, null=True),
        ),
    ]
