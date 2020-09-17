# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-19 06:13

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="ip_address",
        ),
        migrations.AddField(
            model_name="task",
            name="task_notes",
            field=jsonfield.fields.JSONField(default=[]),
        ),
        migrations.AlterField(
            model_name="task",
            name="approved",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="task",
            name="cancelled",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="task",
            name="completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="task",
            name="hash_key",
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name="task",
            name="project_id",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="task_type",
            field=models.CharField(max_length=100),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(fields=["completed"], name="completed_idx"),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(
                fields=["project_id", "uuid"], name="tasks_task_project_a1cfa7_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(
                fields=["project_id", "task_type"], name="tasks_task_project_e86456_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(
                fields=["project_id", "task_type", "cancelled"],
                name="tasks_task_project_f0ec0e_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(
                fields=["project_id", "task_type", "completed", "cancelled"],
                name="tasks_task_project_1cb2a8_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(
                fields=["hash_key", "completed", "cancelled"],
                name="tasks_task_hash_ke_781b6a_idx",
            ),
        ),
    ]
