# Generated by Django 4.2.5 on 2023-09-13 21:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0003_alter_category_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="expense",
            name="description",
            field=models.TextField(null=True),
        ),
    ]
