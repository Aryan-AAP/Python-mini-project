# Generated by Django 5.0.1 on 2024-02-10 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginreg', '0002_quizitem_delete_quizsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizitem',
            name='subject',
            field=models.CharField(default='General', max_length=50),
        ),
    ]
