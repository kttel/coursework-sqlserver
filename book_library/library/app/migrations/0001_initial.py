# Generated by Django 4.0.8 on 2022-11-22 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=255)),
                ('second_name', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=255)),
                ('gender', models.CharField(blank=True, db_collation='Cyrillic_General_CI_AS', max_length=50, null=True)),
                ('birth_date', models.DateField()),
                ('biography', models.TextField(blank=True, db_collation='Cyrillic_General_CI_AS', null=True)),
            ],
            options={
                'db_table': 'author',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=255)),
                ('isbn', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=20, unique=True)),
                ('synopsis', models.TextField(blank=True, db_collation='Cyrillic_General_CI_AS', null=True)),
                ('img', models.BinaryField(blank=True, max_length='max', null=True)),
            ],
            options={
                'db_table': 'book',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'book_author',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BookGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'book_genre',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=75)),
            ],
            options={
                'db_table': 'country',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denomination', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=255)),
            ],
            options={
                'db_table': 'genre',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_time', models.DateTimeField()),
                ('action', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=6)),
                ('entity', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=50)),
                ('username', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=255)),
                ('details', models.TextField(blank=True, db_collation='Cyrillic_General_CI_AS', null=True)),
            ],
            options={
                'db_table': 'log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=255, unique=True)),
                ('accession_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'mailing',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=255)),
                ('content', models.TextField(db_collation='Cyrillic_General_CI_AS')),
                ('published_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'post',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'post_tag',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, db_collation='Cyrillic_General_CI_AS', null=True)),
                ('social_telegram', models.CharField(blank=True, db_collation='Cyrillic_General_CI_AS', max_length=2048, null=True)),
                ('social_twitter', models.CharField(blank=True, db_collation='Cyrillic_General_CI_AS', max_length=2048, null=True)),
                ('social_facebook', models.CharField(blank=True, db_collation='Cyrillic_General_CI_AS', max_length=2048, null=True)),
                ('warnings_amount', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'profile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denomination', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=255)),
            ],
            options={
                'db_table': 'publisher',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=255)),
                ('content', models.TextField(db_collation='Cyrillic_General_CI_AS')),
                ('vote', models.CharField(blank=True, db_collation='Cyrillic_General_CI_AS', max_length=4, null=True)),
                ('moderated', models.BooleanField()),
                ('date_published', models.DateTimeField()),
            ],
            options={
                'db_table': 'review',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denomination', models.CharField(db_collation='Cyrillic_General_CI_AS', max_length=255)),
            ],
            options={
                'db_table': 'tag',
                'managed': False,
            },
        ),
    ]