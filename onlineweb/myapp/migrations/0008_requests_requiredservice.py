# Generated by Django 3.0.5 on 2021-05-31 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_requests'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='requiredservice',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
