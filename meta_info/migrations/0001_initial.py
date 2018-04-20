# Generated by Django 2.0.2 on 2018-04-19 15:51

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageTag',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('copy', models.CharField(db_index=True, max_length=200)),
                ('family', models.TextField(blank=True)),
                ('name_native', models.TextField(blank=True)),
                ('iso_639_1', models.TextField(blank=True)),
                ('iso_639_2_t', models.CharField(db_index=True, max_length=3)),
                ('iso_639_2_b', models.CharField(db_index=True, max_length=3)),
                ('iso_639_3', models.CharField(db_index=True, max_length=9)),
                ('notes', models.TextField(blank=True, default='')),
            ],
            options={
                'verbose_name': 'Language Tag',
                'verbose_name_plural': 'Language Tags',
            },
        ),
        migrations.CreateModel(
            name='LocaliseTag',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='locale_language+', to='meta_info.LanguageTag', verbose_name='Localised Language Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocationTag',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('copy', models.CharField(db_index=True, max_length=200)),
                ('iso_alpha_2', models.CharField(db_index=True, max_length=3)),
                ('iso_alpha_3', models.CharField(db_index=True, max_length=3)),
                ('iso_numeric', models.PositiveIntegerField(blank=True)),
                ('default_language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='default_location_language+', to='meta_info.LanguageTag', verbose_name='Default Location Language')),
                ('parent_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='child_locations+', to='meta_info.LocationTag', verbose_name='Parent Location')),
            ],
            options={
                'verbose_name': 'Location Tag',
                'verbose_name_plural': 'Location Tags',
            },
        ),
        migrations.CreateModel(
            name='MetaInfo',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('copy', models.TextField(blank=True, db_index=True)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
                ('uri', models.URLField(blank=True, max_length=2000, null=True)),
                ('chain', models.ManyToManyField(blank=True, to='meta_info.MetaInfo', verbose_name='Meta Data Chain')),
            ],
            options={
                'verbose_name': 'Meta',
                'verbose_name_plural': 'Metas',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('copy', models.CharField(db_index=True, max_length=200)),
                ('tags', models.ManyToManyField(blank=True, related_name='_tag_tags_+', to='meta_info.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='metainfo',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='_metainfo_tags_+', to='meta_info.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='locationtag',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='_locationtag_tags_+', to='meta_info.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='localisetag',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='locale_language+', to='meta_info.LocationTag', verbose_name='Localised Language Tag'),
        ),
        migrations.AddField(
            model_name='languagetag',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='_languagetag_tags_+', to='meta_info.Tag', verbose_name='Tags'),
        ),
    ]