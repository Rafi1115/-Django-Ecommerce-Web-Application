from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify
from django.db.models.aggregates import (Sum)
from django.template.defaultfilters import truncatechars

class OurUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    image = models.ImageField() # where to upload
    detail = models.TextField()
    f_movie = models.ManyToManyField(to='Movie', 
                related_name='favourite', blank=True)

    country = CountryField()
    region = models.CharField(max_length=250)
    

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'OurUser'
        verbose_name_plural = 'OurUsers'

class PersonManager(models.Manager):
    def all_with_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writers',
            # 'role_set__movie',
            'crew_movie',
            'celebrite_name',
        
            )

class Person(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    country = CountryField()
    image = models.ImageField(null=True, blank=False)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)
    persons = PersonManager()

    def __str__(self):
        if self.died:
            return '{}, {} ({} - {})'.format(
                self.last_name, 
                self.first_name, 
                self.born, 
                self.died
            )
        return '{}, {} ({})'.format(
            self.last_name, 
            self.first_name, 
            self.born
        )
    class Meta:
        db_table = ''
        managed = True
        ordering = ('first_name', 'last_name')
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'




class Movie(models.Model):
    
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - Not rated'),
        (RATED_G, 'G - General Audiences'),
        (RATED_PG, 'PG - Parental Guidance Suggested'),
        (RATED_R, 'R - Restricted'),
    )
    CATEGORY_CHOICES = (
        ('Horror', 'Horror'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Sport', 'Sport'),
        ('WAR', 'WAR'),
        ('Western', 'Western'),
        ('Comedy', 'Comedy'),
        ('Crime', 'Crime'),
        ('Romance', 'Romance'),
        ('Action', 'Action'),
        ('Musicals', 'Musicals'),
    )
    title = models.CharField(max_length=140)
    plot = models.TextField()
    banner = models.ImageField()
    year = models.DateField()
    rating  = models.IntegerField(choices=RATINGS, default=0)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    post = models.BooleanField(default=True)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    slug = models.SlugField(null=False, unique=True)

    # tag = tagmanage
    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name='directed',
        null=True,
        blank=True
    )
    writer = models.ManyToManyField(
        to='Person',
        related_name='writers',
        blank=True
    )

    actors = models.ManyToManyField(
        to='Person',
        through='Role',
        related_name='acting_credits',
        blank=True
    )
    castcrew = models.ManyToManyField(
        to='Person',
        through='Crew',
        related_name='crew_credits',
        blank = True

  
    )
    def get_plot(self):
       return self.plot [:50]
    get_plot.short_plot = "Plot"



    # rating = models.IntegerField(
    #     default=1, validators=[MaxValueValidator(5), MinValueValidator(1)]
    # )

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)

    # def get_absolute_url(self):
    #     return reverse('article_detail', kwargs={'slug': self.slug}) # new

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Movie, self).save(*args, **kwargs)
    
        
    class Meta:
        db_table = ''
        managed = True
        # ordering = ('-year', 'title')
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'   


class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=140)

    def __str__(self):
        return "{} {} {}".format(self.movie_id, self.person_id, self.name)

    class Meta:
        db_table = ''
        managed = True
        unique_together = ('movie', 'person', 'name')   
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

class Crew(models.Model):
    name = models.CharField(max_length=144)
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name='crew_movie')

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Crew'
        verbose_name_plural = 'Crews'


class Celebrite(models.Model):
    name = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name='celebrite_name')
    biography = models.TextField()
    image = models.ImageField()
    movie = models.ManyToManyField(to='Movie', related_name='celebrity_movies')
    spot = models.CharField(max_length=250)
    url = models.URLField(blank=True)

    def __str__(self):
        return str(self.name)


    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Celebrite'
        verbose_name_plural = 'Celebrites'



class TvName(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'TvName'
        verbose_name_plural = 'TvNames'

class TvMovie(models.Model):
    name = models.ForeignKey(TvName, on_delete=models.PROTECT, related_name='tv_names', blank=True, null=True)
    movie = models.ManyToManyField(Movie)
    showtime = models.DateTimeField(auto_now_add=False)


    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'TvMovie'
        verbose_name_plural = 'TvMovies'




class Vote(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    VALUE_CHOISES = (
        ( ONE, "👍" ),  # emojis :)
        ( TWO, "👍👍"),
        ( THREE, "👍👍👍"),
        ( FOUR, "👍👍👍👍"),
        ( FIVE, "👍👍👍👍👍")
    )
    value = models.SmallIntegerField(
        choices=VALUE_CHOISES,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE
    )
    review = models.TextField()
    voted_on = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.movie)

    class Meta:
        db_table = ''
        managed = True
        unique_together = ('user', 'movie')
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

# class TopMovie(models.Model):

#     def __str__(self):
#         pass

#     class Meta:                  # use this from vote model
#         db_table = ''
#         managed = True
#         verbose_name = 'TopMovie'
#         verbose_name_plural = 'TopMovies'


class ComingSoon(models.Model):
    movie = models.ManyToManyField(to='Movie', related_name='coming_movies')
    showtime = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ComingSoon'
        verbose_name_plural = 'ComingSoons'


# class ModelName(models.Model):

#     def __str__(self):
#         pass

#     class Meta:
#         db_table = ''             # use this from vote model
#         managed = True
#         verbose_name = 'ModelName'
#         verbose_name_plural = 'ModelNames'