# Generated by Django 3.1.7 on 2021-03-15 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_name', models.CharField(max_length=255)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo')),
                ('date', models.CharField(max_length=250)),
                ('info', models.TextField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'incident',
                'verbose_name_plural': 'incidents',
            },
        ),
        migrations.CreateModel(
            name='AdvertisementImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='ad_image')),
                ('description', models.CharField(max_length=55)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mysite.advertisement')),
            ],
        ),
        migrations.AddField(
            model_name='advertisement',
            name='incident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.incident'),
        ),
    ]
