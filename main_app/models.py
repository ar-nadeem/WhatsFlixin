from django.db import models

# Create your models here.
class PopularMovie(models.Model):
    poster_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    netflix_url = models.CharField(max_length=500, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'PopularMovies'

class TopMovie(models.Model):
    poster_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    rank = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    netflix_url = models.CharField(max_length=500, default="#")

    def __str__(self):
        return '{} - {}'.format(self.rank, self.title)

    class Meta:
        verbose_name_plural = 'TopMovies'
