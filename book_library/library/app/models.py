# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    first_name = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
    second_name = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
    gender = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS',
                              blank=True, null=True, choices=(('f', 'Female'), ('m', 'Male')))
    birth_date = models.DateField()
    country = models.ForeignKey('Country', models.SET_NULL, db_column='country', blank=True, null=True)
    biography = models.TextField(db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'author'

    def __str__(self):
        return self.first_name + ' ' + self.second_name


class Book(models.Model):
    title = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
    isbn = models.CharField(unique=True, max_length=20, db_collation='Cyrillic_General_CI_AS')
    synopsis = models.TextField(db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    publisher = models.ForeignKey('Publisher', models.SET_NULL, blank=True, null=True)
    img = models.ImageField(blank=True, null=True, upload_to='books/', default='books/default.png')

    class Meta:
        managed = False
        db_table = 'book'

    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, models.CASCADE)
    author = models.ForeignKey(Author, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'book_author'
        unique_together = (('author', 'book'), ('book', 'author'),)

    def __str__(self):
        return str(self.book) + ' (' + str(self.author) + ')'


class BookGenre(models.Model):
    book = models.ForeignKey(Book, models.CASCADE)
    genre = models.ForeignKey('Genre', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'book_genre'
        unique_together = (('genre', 'book'), ('book', 'genre'),)


class Country(models.Model):
    name = models.CharField(max_length=75, db_collation='Cyrillic_General_CI_AS')

    class Meta:
        managed = False
        db_table = 'country'

    def __str__(self):
        return self.name


class Genre(models.Model):
    denomination = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS', unique=True)

    class Meta:
        managed = False
        db_table = 'genre'

    def __str__(self):
        return self.denomination


class Log(models.Model):
    log_time = models.DateTimeField()
    action = models.CharField(max_length=6, db_collation='Cyrillic_General_CI_AS')
    entity = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    username = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
    details = models.TextField(db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log'


class Mailing(models.Model):
    email = models.CharField(unique=True, max_length=255, db_collation='Cyrillic_General_CI_AS')
    accession_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'mailing'

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
    content = models.TextField(db_collation='Cyrillic_General_CI_AS')
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'post'

    def __str__(self):
        return self.title


class PostTag(models.Model):
    post = models.ForeignKey(Post, models.CASCADE)
    tag = models.ForeignKey('Tag', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'post_tag'
        unique_together = (('tag', 'post'), ('post', 'tag'),)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, models.SET_NULL, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    description = models.TextField(db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    social_telegram = models.CharField(max_length=2048, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    social_twitter = models.CharField(max_length=2048, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    social_facebook = models.CharField(max_length=2048, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    warnings_amount = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'profile'

    def __str__(self):
        return self.user.username


class Publisher(models.Model):
    denomination = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')

    class Meta:
        managed = False
        db_table = 'publisher'

    def __str__(self):
        return self.denomination


class Review(models.Model):
    VOTE_CHOICES = [
        ('up', 'Up vote'),
        ('down', 'Down vote'),
    ]

    book = models.ForeignKey(Book, models.DO_NOTHING)
    profile = models.ForeignKey(Profile, models.DO_NOTHING)
    title = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
    content = models.TextField(db_collation='Cyrillic_General_CI_AS')  # This field type is a guess.
    vote = models.CharField(max_length=4, db_collation='Cyrillic_General_CI_AS', blank=True, null=True,
                            choices=VOTE_CHOICES)
    moderated = models.BooleanField(default=0)
    date_published = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'review'
        unique_together = (('book', 'profile'),)

    def __str__(self):
        return self.title


class Tag(models.Model):
    denomination = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS', unique=True)

    class Meta:
        managed = False
        db_table = 'tag'

    def __str__(self):
        return self.denomination
