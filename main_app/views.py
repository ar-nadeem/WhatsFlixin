from django.shortcuts import render

from .models import imdbPopularMovie, imdbTopMovie


# Create your views here.


def imdbPopMovieView(request):

    imdb_Pop_Movie_DB = imdbPopularMovie.objects.all()
    print(imdb_Pop_Movie_DB)

    stuff_for_frontend = {
        'imdb_Pop_Movies': imdb_Pop_Movie_DB,

        'nbar': 'popular',
    }

    return render(request, 'popmovies.html', stuff_for_frontend)


def imdbTopMovieView(request):

    imdb_Top_Movie_DB = imdbTopMovie.objects.all()
    print(imdb_Top_Movie_DB)

    stuff_for_frontend = {
        'imdb_Top_Movies': imdb_Top_Movie_DB,

        'nbar': 'top-rated',
    }

    return render(request, 'topmovies.html', stuff_for_frontend)
