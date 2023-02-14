# Generated by Django 4.1.6 on 2023-02-14 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_comment_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={'permissions': [('is_teacher', 'can access teacher views')]},
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.CharField(max_length=50),
        ),
    ]
