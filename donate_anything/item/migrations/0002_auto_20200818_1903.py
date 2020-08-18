# Generated by Django 3.1 on 2020-08-18 19:03

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="item.item",
            ),
        ),
        migrations.AddField(
            model_name="proposeditem",
            name="item_condition",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveSmallIntegerField(
                    choices=[
                        (0, "Poor"),
                        (1, "Used - Acceptable"),
                        (2, "Used - Very Good"),
                        (3, "Brand New"),
                    ]
                ),
                blank=True,
                default=list,
                size=20000,
            ),
        ),
        migrations.AddField(
            model_name="proposeditem",
            name="names_condition",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveSmallIntegerField(
                    choices=[
                        (0, "Poor"),
                        (1, "Used - Acceptable"),
                        (2, "Used - Very Good"),
                        (3, "Brand New"),
                    ]
                ),
                blank=True,
                default=list,
                size=1500,
            ),
        ),
        migrations.AddField(
            model_name="wanteditem",
            name="condition",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "Poor"),
                    (1, "Used - Acceptable"),
                    (2, "Used - Very Good"),
                    (3, "Brand New"),
                ],
                default=3,
            ),
        ),
        migrations.AlterField(
            model_name="proposeditem",
            name="item",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.BigIntegerField(),
                blank=True,
                default=list,
                size=20000,
            ),
        ),
        migrations.AlterField(
            model_name="proposeditem",
            name="names",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=100),
                blank=True,
                default=list,
                size=1500,
            ),
        ),
    ]
