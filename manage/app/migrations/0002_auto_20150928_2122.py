# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Girlpic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98')),
                ('cl', models.CharField(max_length=20, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb')),
                ('picmsg', models.TextField(verbose_name=b'\xe5\x9b\xbe\xe6\x96\x87\xe5\x88\x97\xe8\xa1\xa8')),
                ('createtime', models.DateField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'db_table': 'girlpic',
                'verbose_name': '\u7f8e\u5973\u56fe\u7247',
                'verbose_name_plural': '\u7f8e\u5973\u56fe\u7247',
            },
        ),
        migrations.AlterModelOptions(
            name='application',
            options={'verbose_name': '\u5f00\u53d1\u8005', 'verbose_name_plural': '\u5f00\u53d1\u8005'},
        ),
        migrations.AlterModelOptions(
            name='content',
            options={'verbose_name': '\u5c0f\u8bf4\u5185\u5bb9', 'verbose_name_plural': '\u5c0f\u8bf4\u5185\u5bb9'},
        ),
        migrations.AlterModelOptions(
            name='novel',
            options={'verbose_name': '\u5c0f\u8bf4\u6807\u9898', 'verbose_name_plural': '\u5c0f\u8bf4\u6807\u9898'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '\u5c0f\u8bf4\u5206\u7c7b', 'verbose_name_plural': '\u5c0f\u8bf4\u5206\u7c7b'},
        ),
        migrations.AlterField(
            model_name='application',
            name='appsecret',
            field=models.CharField(default=b'5ed201a508e874e9ec01765c8db0c42e', unique=True, max_length=32),
        ),
    ]
