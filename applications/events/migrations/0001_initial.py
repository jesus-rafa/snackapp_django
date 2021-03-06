# Generated by Django 3.2.3 on 2021-09-27 23:39

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('description', models.CharField(max_length=254, verbose_name='Descripcion')),
                ('date_start', models.DateField(blank=True, verbose_name='Fecha Inicio')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='Fecha Fin')),
                ('hour_start', models.TimeField(blank=True, null=True, verbose_name='Hora Inicio')),
                ('hour_end', models.TimeField(blank=True, null=True, verbose_name='Hora Fin')),
                ('status', models.CharField(blank=True, max_length=100, verbose_name='Estatus')),
                ('image', models.ImageField(blank=True, null=True, upload_to='events', verbose_name='Imagen')),
                ('is_active', models.BooleanField(default=True)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Eventos',
                'verbose_name_plural': 'Eventos',
            },
        ),
        migrations.CreateModel(
            name='Event_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Contenido')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='events', verbose_name='Imagen 1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='events', verbose_name='Imagen 2')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='events', verbose_name='Imagen 3')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='events', verbose_name='Imagen 4')),
                ('file', models.FileField(blank=True, null=True, upload_to='events', verbose_name='Archivo')),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_event', to='events.event')),
            ],
            options={
                'verbose_name': 'Detalle Eventos',
                'verbose_name_plural': 'Detalle Eventos',
            },
        ),
    ]
