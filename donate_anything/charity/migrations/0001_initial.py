# Generated by Django 3.0.8 on 2020-07-17 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Charity",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("link", models.URLField()),
                ("description", models.TextField(max_length=1000)),
                ("how_to_donate", models.TextField(max_length=300)),
            ],
        ),
    ]
