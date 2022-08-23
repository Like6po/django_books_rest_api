# Generated by Django 4.0 on 2022-08-23 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_token_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время регистрации')),
                ('first_name', models.CharField(max_length=128, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=128, verbose_name='Фамилия')),
                ('password_hash', models.CharField(max_length=256, verbose_name='Хеш пароля')),
                ('role', models.IntegerField(choices=[(0, 'Пользователь'), (1, 'Автор'), (2, 'Администратор')], verbose_name='Роль')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'users',
                'ordering': ['id'],
            },
        ),
    ]
