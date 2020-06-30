from django.db import models


# Create your models here.
class imdbPopMovie(models.Model):
    poster_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.CharField(max_length=5)
    imdb_rating = models.CharField(max_length=10)
    netflix_url = models.CharField(max_length=500, default="#")
    country = models.CharField(max_length=750, default="#")
    release_date = models.CharField(max_length=750, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'PopularMovies'


class imdbTopMovie(models.Model):
    poster_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.CharField(max_length=5)
    imdb_rating = models.CharField(max_length=10)
    netflix_url = models.CharField(max_length=500, default="#")
    country = models.CharField(max_length=750, default="#")
    release_date = models.CharField(max_length=750, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'TopMovies'


class imdbPopTv(models.Model):
    poster_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.CharField(max_length=5)
    imdb_rating = models.CharField(max_length=10)
    netflix_url = models.CharField(max_length=500, default="#")
    country = models.CharField(max_length=750, default="#")
    release_date = models.CharField(max_length=750, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'PopTvs'


class imdbTopTv(models.Model):
    poster_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.CharField(max_length=5)
    imdb_rating = models.CharField(max_length=10)
    netflix_url = models.CharField(max_length=500, default="#")
    country = models.CharField(max_length=750, default="#")
    release_date = models.CharField(max_length=750, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'TopTvs'
