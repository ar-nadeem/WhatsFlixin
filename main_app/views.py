from django.shortcuts import render
from .models import imdbPopMovie, imdbTopMovie, imdbPopTv, imdbTopTv


# Create your views here.

def imdbPopMovieView(request):
    arrow ="up"
    button_pressed ="rank"
    only_arrow_post = False
    country = "N/A"


    imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('rank')

    if request.POST.get('action') == 'post':

        try:
            button_post = request.POST['button_post']
            button_pressed = button_post

        except :
            only_arrow_post = True
            arrow_post = request.POST['arrow_post']
            if arrow_post == "up":
                arrow = "down"
            else:
                arrow = "up"



        if only_arrow_post:
            if request.POST['rank'].find("disabled") > -1:
                button_pressed = "rank"
            if request.POST['avail'].find("disabled") > -1:
                button_pressed = "avail"
            if request.POST['reldate'].find("disabled") > -1:
                button_pressed = "reldate"

        if button_pressed == "reldate":
            if arrow == "up":
                imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('release_date')
            else:
                imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('-release_date')

        if button_pressed == "rank":
            if arrow == "up":
                imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('rank')
            else:
                imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('-rank')

        if button_pressed == "avail":
            country = request.POST['country']
            if country == "Pakistan":
                country = "India"

            print(country)
            imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('rank')
            wanted_items = set()
            not_wanted_items = set()
            for models in imdb_Pop_Movie_DB:
                if models.country.find(country) >= 0:
                    wanted_items.add(models.pk)
                else:
                    not_wanted_items.add(models.pk)
            if arrow == "up":
                imdb_Pop_Movie_DB= imdbPopMovie.objects.filter(pk__in=wanted_items)
            else:
                imdb_Pop_Movie_DB = imdbPopMovie.objects.filter(pk__in=not_wanted_items)





    stuff_for_frontend = {
        'imdb_Pop_Movies': imdb_Pop_Movie_DB,
        'nbar': 'popm',
        'arrow_pos': arrow,
        'button_disabled': button_pressed,
        'country': country,

    }

    return render(request, 'popmovies.html', stuff_for_frontend)



def imdbTopMovieView(request):
    arrow ="up"
    button_pressed ="rank"
    only_arrow_post = False
    country = "N/A"

    imdb_Top_Movie_DB = imdbTopMovie.objects.all().order_by('rank')

    if request.POST.get('action') == 'post':

        try:
            button_post = request.POST['button_post']
            button_pressed = button_post

        except :
            only_arrow_post = True
            arrow_post = request.POST['arrow_post']
            if arrow_post == "up":
                arrow = "down"
            else:
                arrow = "up"



        if only_arrow_post:
            if request.POST['rank'].find("disabled") > -1:
                button_pressed = "rank"
            if request.POST['avail'].find("disabled") > -1:
                button_pressed = "avail"
            if request.POST['reldate'].find("disabled") > -1:
                button_pressed = "reldate"

    if button_pressed == "reldate":
        if arrow == "up":
            imdb_Top_Movie_DB = imdbTopMovie.objects.all().order_by('release_date')
        else:
            imdb_Top_Movie_DB = imdbTopMovie.objects.all().order_by('-release_date')

    if button_pressed == "rank":
        if arrow == "up":
            imdb_Top_Movie_DB = imdbTopMovie.objects.all().order_by('rank')
        else:
            imdb_Top_Movie_DB = imdbTopMovie.objects.all().order_by('-rank')

    if button_pressed == "avail":
        country = request.POST['country']
        if country == "Pakistan":
            country = "India"

        print(country)
        imdb_Top_Movie_DB = imdbTopMovie.objects.all().order_by('rank')
        wanted_items = set()
        not_wanted_items = set()
        for models in imdb_Top_Movie_DB:
            if models.country.find(country) >= 0:
                wanted_items.add(models.pk)
            else:
                not_wanted_items.add(models.pk)
        if arrow == "up":
            imdb_Top_Movie_DB = imdbTopMovie.objects.filter(pk__in=wanted_items)
        else:
            imdb_Top_Movie_DB = imdbTopMovie.objects.filter(pk__in=not_wanted_items)

    stuff_for_frontend = {
        'imdb_Top_Movies': imdb_Top_Movie_DB,
        'nbar': 'topm',
        'arrow_pos': arrow,
        'button_disabled': button_pressed,
        'country':country,
    }

    return render(request, 'topmovies.html', stuff_for_frontend)



############################### TV #########################################

def imdbPopTvView(request):
    arrow ="up"
    button_pressed ="rank"
    only_arrow_post = False
    country = "N/A"

    imdb_Pop_Tv_DB = imdbPopTv.objects.all().order_by('rank')


    if request.POST.get('action') == 'post':

        try:
            button_post = request.POST['button_post']
            button_pressed = button_post

        except :
            only_arrow_post = True
            arrow_post = request.POST['arrow_post']
            if arrow_post == "up":
                arrow = "down"
            else:
                arrow = "up"



        if only_arrow_post:
            if request.POST['rank'].find("disabled") > -1:
                button_pressed = "rank"
            if request.POST['avail'].find("disabled") > -1:
                button_pressed = "avail"
            if request.POST['reldate'].find("disabled") > -1:
                button_pressed = "reldate"
    if button_pressed == "reldate":
        if arrow == "up":
            imdb_Pop_Tv_DB = imdbPopTv.objects.all().order_by('release_date')
        else:
            imdb_Pop_Tv_DB = imdbPopTv.objects.all().order_by('-release_date')

    if button_pressed == "rank":
        if arrow == "up":
            imdb_Pop_Tv_DB = imdbPopTv.objects.all().order_by('rank')
        else:
            imdb_Pop_Tv_DB = imdbPopTv.objects.all().order_by('-rank')

    if button_pressed == "avail":
        country = request.POST['country']
        if country == "Pakistan":
            country = "India"

        print(country)
        imdb_Pop_Tv_DB = imdbPopTv.objects.all().order_by('rank')
        wanted_items = set()
        not_wanted_items = set()
        for models in imdb_Pop_Tv_DB:
            if models.country.find(country) >= 0:
                wanted_items.add(models.pk)
            else:
                not_wanted_items.add(models.pk)
        if arrow == "up":
            imdb_Pop_Tv_DB = imdbPopTv.objects.filter(pk__in=wanted_items)
        else:
            imdb_Pop_Tv_DB = imdbPopTv.objects.filter(pk__in=not_wanted_items)

    stuff_for_frontend = {
        'imdb_Pop_Tv': imdb_Pop_Tv_DB,
        'nbar': 'poptv',
        'arrow_pos': arrow,
        'button_disabled': button_pressed,
        'country':country,

    }

    return render(request, 'poptv.html', stuff_for_frontend)




def imdbTopTvView(request):
    arrow ="up"
    button_pressed ="rank"
    only_arrow_post = False
    country = "N/A"

    imdb_Top_Tv_DB = imdbTopTv.objects.all().order_by('rank')


    if request.POST.get('action') == 'post':

        try:
            button_post = request.POST['button_post']
            button_pressed = button_post

        except :
            only_arrow_post = True
            arrow_post = request.POST['arrow_post']
            if arrow_post == "up":
                arrow = "down"
            else:
                arrow = "up"



        if only_arrow_post:
            if request.POST['rank'].find("disabled") > -1:
                button_pressed = "rank"
            if request.POST['avail'].find("disabled") > -1:
                button_pressed = "avail"
            if request.POST['reldate'].find("disabled") > -1:
                button_pressed = "reldate"

    if button_pressed == "reldate":
        if arrow == "up":
            imdb_Top_Tv_DB = imdbTopTv.objects.all().order_by('release_date')
        else:
            imdb_Top_Tv_DB = imdbTopTv.objects.all().order_by('-release_date')

    if button_pressed == "rank":
        if arrow == "up":
            imdb_Top_Tv_DB = imdbTopTv.objects.all().order_by('rank')
        else:
            imdb_Top_Tv_DB = imdbTopTv.objects.all().order_by('-rank')

    if button_pressed == "avail":
        country = request.POST['country']
        if country == "Pakistan":
            country = "India"

        print(country)
        imdb_Top_Tv_DB = imdbTopTv.objects.all().order_by('rank')
        wanted_items = set()
        not_wanted_items = set()
        for models in imdb_Top_Tv_DB:
            if models.country.find(country) >= 0:
                wanted_items.add(models.pk)
            else:
                not_wanted_items.add(models.pk)
        if arrow == "up":
            imdb_Top_Tv_DB = imdbTopTv.objects.filter(pk__in=wanted_items)
        else:
            imdb_Top_Tv_DB = imdbTopTv.objects.filter(pk__in=not_wanted_items)


    stuff_for_frontend = {
        'imdb_Top_Tv': imdb_Top_Tv_DB,
        'nbar': 'toptv',
        'arrow_pos': arrow,
        'button_disabled': button_pressed,
        'country':country,
    }

    return render(request, 'toptv.html', stuff_for_frontend)
