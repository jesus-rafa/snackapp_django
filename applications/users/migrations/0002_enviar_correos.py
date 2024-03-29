# Generated by Django 3.2.3 on 2022-07-10 22:39

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enviar_Correos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('correo', models.EmailField(blank=True, max_length=200, verbose_name='Correo')),
                ('nombre', models.CharField(blank=True, max_length=200, verbose_name='Nombre')),
                ('password', models.CharField(blank=True, max_length=50, verbose_name='Nombre')),
                ('tipo', models.CharField(blank=True, max_length=200, verbose_name='Tipo')),
                ('is_sent', models.BooleanField(default=False)),
                ('id_evento', models.CharField(blank=True, max_length=10, verbose_name='id evento')),
                ('comentarios', models.CharField(blank=True, max_length=800, null=True, verbose_name='Comentarios')),
            ],
            options={
                'verbose_name': 'Enviar_Correos',
                'verbose_name_plural': 'Enviar_Correos',
                'ordering': ['correo'],
            },
        ),
    ]
