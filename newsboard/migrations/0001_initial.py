# Generated by Django 4.2.7 on 2023-11-09 13:30

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Tanks', 'Танки'), ('Heals', 'Хилы'), ('Damage Dealers', 'ДД'), ('Traders', 'Торговцы'), ('Guildmasters', 'Гилдмастеры'), ('Questgivers', 'Квестгиверы'), ('Blacksmiths', 'Кузнецы'), (' Tanners', ' Кожевники'), ('Potions makers', 'Зельевары'), ('Spell masters', 'Мастера заклинаний')], default='Tanks', max_length=64)),
                ('title', models.CharField(max_length=100)),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('time_in', models.DateTimeField(auto_now_add=True)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsboard.category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsboard.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('time_in', models.DateTimeField(auto_now_add=True)),
                ('comment_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsboard.post')),
            ],
        ),
        migrations.CreateModel(
            name='CategorySubscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsboard.category')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(through='newsboard.CategorySubscribe', to=settings.AUTH_USER_MODEL),
        ),
    ]
