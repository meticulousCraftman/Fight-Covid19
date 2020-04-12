# Generated by Django 2.2.11 on 2020-04-12 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("maps", "0010_healthentry_unique_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="HelpEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fullname", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=15)),
                (
                    "help_type",
                    models.CharField(
                        choices=[
                            ("food_donation", "Food Donation"),
                            ("grocery_store", "Grocery Store"),
                            ("medical_store", "Medical Store"),
                            ("other", "Other"),
                        ],
                        default="food_donation",
                        max_length=10,
                    ),
                ),
                ("address", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "latitude",
                    models.DecimalField(decimal_places=15, max_digits=18, null=True),
                ),
                (
                    "longitude",
                    models.DecimalField(decimal_places=15, max_digits=18, null=True),
                ),
                (
                    "creation_timestamp",
                    models.DateTimeField(auto_now_add=True, null=True),
                ),
            ],
        ),
    ]
