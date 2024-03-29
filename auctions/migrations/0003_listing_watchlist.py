# Generated by Django 4.1.5 on 2023-04-09 22:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_alter_listing_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="watchlist",
            field=models.ManyToManyField(
                related_name="watchlist", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
