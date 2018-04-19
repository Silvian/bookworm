# Generated by Django 2.0.2 on 2018-04-19 15:51

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meta_info', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMethod',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('copy', models.TextField(blank=True, db_index=True)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
                ('type', models.IntegerField(blank=True, choices=[(0, 'email'), (1, 'mobile number'), (2, 'landline number'), (3, 'postal address'), (4, 'billing address'), (5, 'social network id')], default=0)),
                ('detail', models.TextField(db_index=True)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, null=True)),
                ('uri', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Contact Method',
                'verbose_name_plural': 'Contact Methods',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('name_title', models.IntegerField(blank=True, choices=[(0, 'Mrs'), (1, 'Mr'), (2, 'Miss'), (3, 'Ms'), (4, 'Dr'), (5, 'Sir')], null=True)),
                ('name_first', models.CharField(db_index=True, max_length=64)),
                ('name_family', models.CharField(db_index=True, max_length=64)),
                ('name_middle', models.CharField(blank=True, max_length=128, null=True)),
                ('name_display', models.CharField(blank=True, max_length=254)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('meta_info', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile_meta+', to='meta_info.MetaInfo', verbose_name='Profile meta data')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name="Profiles' User")),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.AddField(
            model_name='contactmethod',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='contacts', to='authentication.Profile', verbose_name='Contact details profile'),
        ),
        migrations.AddField(
            model_name='contactmethod',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='_contactmethod_tags_+', to='meta_info.Tag', verbose_name='Tags'),
        ),
    ]
