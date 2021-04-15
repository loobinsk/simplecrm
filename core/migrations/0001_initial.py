# Generated by Django 3.0 on 2021-04-14 14:00

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
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.FileField(upload_to='records/%m/')),
                ('call_date', models.DateTimeField()),
                ('call_status', models.SmallIntegerField(blank=True, choices=[(0, 'отвеченно'), (1, 'Не дозвонился'), (2, 'Занято')], default=0)),
            ],
            options={
                'verbose_name': 'Звонок',
                'verbose_name_plural': 'Звонки',
                'ordering': ('-call_date',),
            },
        ),
        migrations.CreateModel(
            name='Ddd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('name2', models.CharField(max_length=234)),
            ],
        ),
        migrations.CreateModel(
            name='SelectedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data1', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('call_source', models.CharField(default='не определен', max_length=255)),
                ('current_situation', models.TextField(blank=True)),
                ('desired_situation', models.TextField(blank=True)),
                ('other_options', models.TextField(blank=True)),
                ('main_motive', models.TextField(blank=True)),
                ('proposed', models.TextField(blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, default='slug', max_length=255)),
                ('curator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ('-create_date',),
            },
        ),
        migrations.CreateModel(
            name='CallComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.Call')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('call',),
            },
        ),
        migrations.AddField(
            model_name='call',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls', to='core.Client'),
        ),
        migrations.AddField(
            model_name='call',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
