from django.db import models


# Create your models here.
class imdbPopularMovie(models.Model):

    poster_link = models.CharField(max_length=1000)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.CharField(max_length=100)
    imdb_rating = models.CharField(max_length=100)
    netflix_url = models.CharField(max_length=500, default="#")
    country = models.CharField(max_length=2000, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'PopularMovies'


class imdbTopMovie(models.Model):
    poster_link = models.CharField(max_length=1000)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.CharField(max_length=100)
    imdb_rating = models.CharField(max_length=100)
    netflix_url = models.CharField(max_length=500, default="#")
    country = models.CharField(max_length=500, default="#")


    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'TopMovies'
