from django.shortcuts import render

from .models import PopularMovie, TopMovie



# Create your views here.


def PopView(request):


    data = PopularMovie.objects.all()
    print(data)

    stuff_for_frontend = {
        'Pmovie_post': data,

        'nbar': 'popular',
    }


    return render(request, 'popmovies.html', stuff_for_frontend)





def TopView(request):
    data = TopMovie.objects.all()
    print(data)

    stuff_for_frontend = {
        'Tmovie_post': data,

        'nbar': 'top-rated',
    }

    return render(request, 'topmovies.html', stuff_for_frontend)
