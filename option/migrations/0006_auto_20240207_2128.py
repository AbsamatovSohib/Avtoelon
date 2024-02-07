# Generated by Django 3.2 on 2024-02-07 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0005_alter_postoption_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='is_filter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='option',
            name='is_main',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='optionvalueextended',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='option.optionvalueextended'),
        ),
        migrations.AlterField(
            model_name='postoptionvalue',
            name='post_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='option.postoption'),
        ),
    ]