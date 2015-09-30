# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appsecret', models.CharField(default=b'c5758668252aed1ac8bfd68a93df5c0b', unique=True, max_length=32)),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'application',
                'verbose_name': '\u5e94\u7528',
                'verbose_name_plural': '\u5e94\u7528',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('novelid', models.IntegerField(verbose_name=b'\xe5\xb0\x8f\xe8\xaf\xb4ID', db_index=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98', db_index=True)),
                ('first', models.IntegerField(verbose_name=b'\xe4\xb8\x80\xe7\xba\xa7\xe5\x88\x86\xe7\xb1\xbb', db_index=True)),
                ('second', models.IntegerField(verbose_name=b'\xe4\xba\x8c\xe7\xba\xa7\xe5\x88\x86\xe7\xb1\xbb', db_index=True)),
                ('chapter', models.IntegerField(verbose_name=b'\xe5\xba\x8f\xe5\x88\x97', db_index=True)),
                ('subtitle', models.CharField(max_length=200, verbose_name=b'\xe5\x89\xaf\xe6\xa0\x87\xe9\xa2\x98', db_index=True)),
                ('text', models.TextField(verbose_name=b'\xe6\xad\xa3\xe6\x96\x87')),
                ('contentsource', models.CharField(max_length=300, verbose_name=b'\xe5\x8e\x9f\xe6\x96\x87\xe5\x9c\xb0\xe5\x9d\x80')),
                ('createtime', models.DateField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'db_table': 'content',
                'verbose_name': '\u5185\u5bb9',
                'verbose_name_plural': '\u5185\u5bb9',
            },
        ),
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98')),
                ('first', models.IntegerField(verbose_name=b'\xe4\xb8\x80\xe7\xba\xa7\xe5\x88\x86\xe7\xb1\xbb', db_index=True)),
                ('second', models.IntegerField(verbose_name=b'\xe4\xba\x8c\xe7\xba\xa7\xe5\x88\x86\xe7\xb1\xbb', db_index=True)),
                ('author', models.CharField(max_length=50, verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85', db_index=True)),
                ('introduction', models.TextField(verbose_name=b'\xe4\xbd\x9c\xe5\x93\x81\xe7\xae\x80\xe4\xbb\x8b')),
                ('picture', models.CharField(max_length=300, verbose_name=b'\xe5\x9b\xbe\xe7\x89\x87')),
                ('novelsource', models.CharField(max_length=300, verbose_name=b'\xe5\x8e\x9f\xe6\x96\x87\xe5\x9c\xb0\xe5\x9d\x80')),
                ('createtime', models.DateField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'db_table': 'novel',
                'verbose_name': '\u5c0f\u8bf4',
                'verbose_name_plural': '\u5c0f\u8bf4',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first', models.IntegerField(db_index=True, verbose_name=b'\xe4\xb8\x80\xe7\xba\xa7\xe5\x88\x86\xe7\xb1\xbb', choices=[[0, b'\xe5\xa5\xb3'], [1, b'\xe7\x94\xb7']])),
                ('second', models.CharField(unique=True, max_length=200, verbose_name=b'\xe4\xba\x8c\xe7\xba\xa7\xe5\x88\x86\xe7\xb1\xbb')),
                ('createtime', models.DateField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'db_table': 'tag',
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
    ]
