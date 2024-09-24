# Generated by Django 4.2.4 on 2024-09-24 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0003_hyperlink_article_name_alter_article_hyperlinks'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='contents',
            field=models.ManyToManyField(blank=True, related_name='articles', to='directory.content'),
        ),
    ]
