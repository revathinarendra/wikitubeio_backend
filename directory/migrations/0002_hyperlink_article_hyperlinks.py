# Generated by Django 4.2.4 on 2024-09-24 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hyperlink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hyper_link_word', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('hyper_link_word_url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='hyperlinks',
            field=models.ManyToManyField(blank=True, to='directory.hyperlink'),
        ),
    ]
