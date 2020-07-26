from django.db import models


# Create your models here.
class imdbPopMovie(models.Model):
    poster_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.IntegerField(blank=True, null=True)
    imdb_rating = models.FloatField(max_length=10, default="0.0")
    rotten_rating = models.CharField(max_length=10, default="#")
    meta_rating = models.CharField(max_length=10, default="#")
    netflix_url = models.CharField(max_length=500, default="#")
    country = models.CharField(max_length=750, default="#")
    release_date = models.IntegerField(blank=True, null=True)
    trailer_url = models.CharField(max_length=750, default="#")
    imdb_url = models.CharField(max_length=500, default="#")
    rotten_url = models.CharField(max_length=500, default="#")
    meta_url = models.CharField(max_length=500, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'PopularMovies'


class imdbTopMovie(models.Model):
    poster_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.IntegerField(blank=True, null=True)
    imdb_rating = models.FloatField(max_length=10, default="0.0")
    rotten_rating = models.CharField(max_length=10, default="#")
    meta_rating = models.CharField(max_length=10, default="#")
    netflix_url = models.CharField(max_length=500, default="#")
    imdb_url = models.CharField(max_length=500, default="#")
    rotten_url = models.CharField(max_length=500, default="#")
    meta_url = models.CharField(max_length=500, default="#")
    country = models.CharField(max_length=750, default="#")
    release_date = models.IntegerField(blank=True, null=True)
    trailer_url = models.CharField(max_length=750, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'TopMovies'


class imdbPopTv(models.Model):
    poster_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.IntegerField(blank=True, null=True)
    imdb_rating = models.FloatField(max_length=10, default="0.0")
    rotten_rating = models.CharField(max_length=10, default="#")
    meta_rating = models.CharField(max_length=10, default="#")
    netflix_url = models.CharField(max_length=500, default="#")
    country = models.CharField(max_length=750, default="#")
    release_date = models.IntegerField(blank=True, null=True)
    trailer_url = models.CharField(max_length=750, default="#")
    imdb_url = models.CharField(max_length=500, default="#")
    rotten_url = models.CharField(max_length=500, default="#")
    meta_url = models.CharField(max_length=500, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'PopTvs'


class imdbTopTv(models.Model):
    poster_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.IntegerField(blank=True, null=True)
    imdb_rating = models.FloatField(max_length=10, default="0.0")
    rotten_rating = models.CharField(max_length=10, default="#")
    meta_rating = models.CharField(max_length=10, default="#")
    netflix_url = models.CharField(max_length=500, default="#")
    country = models.CharField(max_length=750, default="#")
    release_date = models.IntegerField(blank=True, null=True)
    trailer_url = models.CharField(max_length=750, default="#")
    imdb_url = models.CharField(max_length=500, default="#")
    rotten_url = models.CharField(max_length=500, default="#")
    meta_url = models.CharField(max_length=500, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'TopTvs'
