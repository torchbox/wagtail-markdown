# Generated by Django 3.2.4 on 2021-06-18 11:36

import django.db.models.deletion
from django.db import migrations, models
from wagtail import fields as wagtail_fields

import wagtailmarkdown.blocks
import wagtailmarkdown.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0059_apply_collection_ordering"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("body", wagtailmarkdown.fields.MarkdownField(blank=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="TestWithStreamFieldPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail_fields.StreamField(
                        [
                            (
                                "markdown",
                                wagtailmarkdown.blocks.MarkdownBlock(icon="code"),
                            )
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
