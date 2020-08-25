from django.shortcuts import render
from .models import imdbPopMovie, imdbTopMovie, imdbPopTv, imdbTopTv
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponse

# Create your views here.
def AdsView(request):
    line = "google.com, pub-7803878263219083, DIRECT, f08c47fec0942fa0"
    return HttpResponse(line)


def imdbPopMovieView(request):
    ip = ""
    arrow ="up"
    button_pressed = "List Rank"
    last_pressed = "List Rank"
    only_arrow_post = False
    country = "N/A"
    region_filter = False
    double_pressed = False

    if button_pressed == "List Rank":
        imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('rank')

    if request.POST.get('action') == 'post':
        last_pressed = request.POST['last_pressed']
        try:
            button_pressed = request.POST['button_post']
            if button_pressed == "IMDB Rating":
                arrow = "down"
            if button_pressed == "avail":
                if button_pressed == "IMDB Rating":
                    arrow = "down"
                if request.POST['avail'].find("disabled") > 0:
                    double_pressed = True
                    region_filter = False
                    button_pressed = last_pressed
                else:
                    region_filter = True
                    button_pressed = last_pressed

            print(button_pressed)

        except :
            only_arrow_post = True
            arrow_post = request.POST['arrow_post']
            if arrow_post == "up":
                arrow = "down"
            else:
                arrow = "up"
            try:
                if request.POST['avail'].find("disabled") > 0:
                    region_filter = True
                    button_pressed = last_pressed
                else:
                    region_filter = False
            except:
                pass


        if request.POST['avail'].find("disabled") > 0 and double_pressed != True:
            region_filter = True



        if only_arrow_post :
            button_pressed = last_pressed

        if button_pressed == "Release Date":
            if arrow == "up":
                imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('release_date')
            else:
                imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('-release_date')

        if button_pressed == "List Rank":
            if arrow == "up":
                imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('rank')
            else:
                imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('-rank')

        if button_pressed == "IMDB Rating":
            if arrow == "up":
                imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('imdb_rating')
            else:
                imdb_Pop_Movie_DB = imdbPopMovie.objects.all().order_by('-imdb_rating')

        if region_filter:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            if ip == "127.0.0.1":
                ip = "72.255.7.40"

            country = GeoIP2().city(ip)['country_name']


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

            if button_pressed == "Release Date":
                if arrow == "up":
                    imdb_Pop_Movie_DB = imdbPopMovie.objects.filter(pk__in=wanted_items).order_by('release_date')
                else:
                    imdb_Pop_Movie_DB = imdbPopMovie.objects.filter(pk__in=wanted_items).order_by('-release_date')

            if button_pressed == "List Rank":
                if arrow == "up":
                    imdb_Pop_Movie_DB = imdbPopMovie.objects.filter(pk__in=wanted_items).order_by('rank')
                else:
                    imdb_Pop_Movie_DB = imdbPopMovie.objects.filter(pk__in=wanted_items).order_by('-rank')

            if button_pressed == "IMDB Rating":
                if arrow == "up":
                    imdb_Pop_Movie_DB = imdbPopMovie.objects.filter(pk__in=wanted_items).order_by('imdb_rating')
                else:
                    imdb_Pop_Movie_DB = imdbPopMovie.objects.filter(pk__in=wanted_items).order_by('-imdb_rating')


    stuff_for_frontend = {
        'imdb_Pop_Movies': imdb_Pop_Movie_DB,
        'nbar': 'popm',
        'arrow_pos': arrow,
        'button_disabled': button_pressed,
        'country': country,
        'region_filter': region_filter,
        "ip": ip,

    }

    return render(request, 'popmovies.html', stuff_for_frontend)



def imdbTopMovieView(request):
    arrow = "up"
    button_pressed = "List Rank"
    last_pressed = "List Rank"
    only_arrow_post = False
    country = "N/A"
    region_filter = False
    double_pressed = False

    if button_pressed == "List Rank":
        imdb_Top_Movies = imdbTopMovie.objects.all().order_by('rank')

    if request.POST.get('action') == 'post':
        last_pressed = request.POST['last_pressed']
        try:
            button_pressed = request.POST['button_post']
            if button_pressed == "IMDB Rating":
                arrow = "down"
            if button_pressed == "avail":
                if button_pressed == "IMDB Rating":
                    arrow = "down"
                if request.POST['avail'].find("disabled") > 0:
                    double_pressed = True
                    region_filter = False
                    button_pressed = last_pressed
                else:
                    region_filter = True
                    button_pressed = last_pressed

            print(button_pressed)

        except:
            only_arrow_post = True
            arrow_post = request.POST['arrow_post']
            if arrow_post == "up":
                arrow = "down"
            else:
                arrow = "up"
            try:
                if request.POST['avail'].find("disabled") > 0:
                    region_filter = True
                    button_pressed = last_pressed
                else:
                    region_filter = False
            except:
                pass

        if request.POST['avail'].find("disabled") > 0 and double_pressed != True:
            region_filter = True

        if only_arrow_post:
            button_pressed = last_pressed

        if button_pressed == "Release Date":
            if arrow == "up":
                imdb_Top_Movies = imdbTopMovie.objects.all().order_by('release_date')
            else:
                imdb_Top_Movies = imdbTopMovie.objects.all().order_by('-release_date')

        if button_pressed == "List Rank":
            if arrow == "up":
                imdb_Top_Movies = imdbTopMovie.objects.all().order_by('rank')
            else:
                imdb_Top_Movies = imdbTopMovie.objects.all().order_by('-rank')

        if button_pressed == "IMDB Rating":
            if arrow == "up":
                imdb_Top_Movies = imdbTopMovie.objects.all().order_by('imdb_rating')
            else:
                imdb_Top_Movies = imdbTopMovie.objects.all().order_by('-imdb_rating')

        if region_filter:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            if ip == "127.0.0.1":
                ip = "72.255.7.40"

            country = GeoIP2().city(ip)['country_name']

            if country == "Pakistan":
                country = "India"

            print(country)
            imdb_Top_Movies = imdbTopMovie.objects.all().order_by('rank')
            wanted_items = set()
            not_wanted_items = set()
            for models in imdb_Top_Movies:
                if models.country.find(country) >= 0:
                    wanted_items.add(models.pk)
                else:
                    not_wanted_items.add(models.pk)

            if button_pressed == "Release Date":
                if arrow == "up":
                    imdb_Top_Movies = imdbTopMovie.objects.filter(pk__in=wanted_items).order_by('release_date')
                else:
                    imdb_Top_Movies = imdbTopMovie.objects.filter(pk__in=wanted_items).order_by('-release_date')

            if button_pressed == "List Rank":
                if arrow == "up":
                    imdb_Top_Movies = imdbTopMovie.objects.filter(pk__in=wanted_items).order_by('rank')
                else:
                    imdb_Top_Movies = imdbTopMovie.objects.filter(pk__in=wanted_items).order_by('-rank')

            if button_pressed == "IMDB Rating":
                if arrow == "up":
                    imdb_Top_Movies = imdbTopMovie.objects.filter(pk__in=wanted_items).order_by('imdb_rating')
                else:
                    imdb_Top_Movies = imdbTopMovie.objects.filter(pk__in=wanted_items).order_by('-imdb_rating')

    stuff_for_frontend = {
        'imdb_Top_Movies': imdb_Top_Movies,
        'nbar': 'topm',
        'arrow_pos': arrow,
        'button_disabled': button_pressed,
        'country': country,
        'region_filter': region_filter,

    }

    return render(request, 'topmovies.html', stuff_for_frontend)



############################### TV #########################################

def imdbPopTvView(request):
    arrow = "up"
    button_pressed = "List Rank"
    last_pressed = "List Rank"
    only_arrow_post = False
    country = "N/A"
    region_filter = False
    double_pressed = False

    if button_pressed == "List Rank":
        imdb_Pop_Tv = imdbPopTv.objects.all().order_by('rank')

    if request.POST.get('action') == 'post':
        last_pressed = request.POST['last_pressed']
        try:
            button_pressed = request.POST['button_post']
            if button_pressed == "IMDB Rating":
                arrow = "down"
            if button_pressed == "avail":
                if button_pressed == "IMDB Rating":
                    arrow = "down"
                if request.POST['avail'].find("disabled") > 0:
                    double_pressed = True
                    region_filter = False
                    button_pressed = last_pressed
                else:
                    region_filter = True
                    button_pressed = last_pressed

            print(button_pressed)

        except:
            only_arrow_post = True
            arrow_post = request.POST['arrow_post']
            if arrow_post == "up":
                arrow = "down"
            else:
                arrow = "up"
            try:
                if request.POST['avail'].find("disabled") > 0:
                    region_filter = True
                    button_pressed = last_pressed
                else:
                    region_filter = False
            except:
                pass

        if request.POST['avail'].find("disabled") > 0 and double_pressed != True:
            region_filter = True

        if only_arrow_post:
            button_pressed = last_pressed

        if button_pressed == "Release Date":
            if arrow == "up":
                imdb_Pop_Tv = imdbPopTv.objects.all().order_by('release_date')
            else:
                imdb_Pop_Tv = imdbPopTv.objects.all().order_by('-release_date')

        if button_pressed == "List Rank":
            if arrow == "up":
                imdb_Pop_Tv = imdbPopTv.objects.all().order_by('rank')
            else:
                imdb_Pop_Tv = imdbPopTv.objects.all().order_by('-rank')

        if button_pressed == "IMDB Rating":
            if arrow == "up":
                imdb_Pop_Tv = imdbPopTv.objects.all().order_by('imdb_rating')
            else:
                imdb_Pop_Tv = imdbPopTv.objects.all().order_by('-imdb_rating')

        if region_filter:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            if ip == "127.0.0.1":
                ip = "72.255.7.40"
            country = GeoIP2().city(ip)['country_name']

            if country == "Pakistan":
                country = "India"

            print(country)
            imdb_Pop_Tv = imdbPopTv.objects.all().order_by('rank')
            wanted_items = set()
            not_wanted_items = set()
            for models in imdb_Pop_Tv:
                if models.country.find(country) >= 0:
                    wanted_items.add(models.pk)
                else:
                    not_wanted_items.add(models.pk)

            if button_pressed == "Release Date":
                if arrow == "up":
                    imdb_Pop_Tv = imdbPopTv.objects.filter(pk__in=wanted_items).order_by('release_date')
                else:
                    imdb_Pop_Tv = imdbPopTv.objects.filter(pk__in=wanted_items).order_by('-release_date')

            if button_pressed == "List Rank":
                if arrow == "up":
                    imdb_Pop_Tv = imdbPopTv.objects.filter(pk__in=wanted_items).order_by('rank')
                else:
                    imdb_Pop_Tv = imdbPopTv.objects.filter(pk__in=wanted_items).order_by('-rank')

            if button_pressed == "IMDB Rating":
                if arrow == "up":
                    imdb_Pop_Tv = imdbPopTv.objects.filter(pk__in=wanted_items).order_by('imdb_rating')
                else:
                    imdb_Pop_Tv = imdbPopTv.objects.filter(pk__in=wanted_items).order_by('-imdb_rating')

    stuff_for_frontend = {
        'imdb_Pop_Tv': imdb_Pop_Tv,
        'nbar': 'poptv',
        'arrow_pos': arrow,
        'button_disabled': button_pressed,
        'country': country,
        'region_filter': region_filter,


    }

    return render(request, 'poptv.html', stuff_for_frontend)




def imdbTopTvView(request):
    arrow = "up"
    button_pressed = "List Rank"
    last_pressed = "List Rank"
    only_arrow_post = False
    country = "N/A"
    region_filter = False
    double_pressed = False

    if button_pressed == "List Rank":
        imdb_Top_Tv = imdbTopTv.objects.all().order_by('rank')

    if request.POST.get('action') == 'post':
        last_pressed = request.POST['last_pressed']
        try:
            button_pressed = request.POST['button_post']
            if button_pressed == "IMDB Rating":
                arrow = "down"
            if button_pressed == "avail":
                if button_pressed == "IMDB Rating":
                    arrow = "down"
                if request.POST['avail'].find("disabled") > 0:
                    double_pressed = True
                    region_filter = False
                    button_pressed = last_pressed
                else:
                    region_filter = True
                    button_pressed = last_pressed

            print(button_pressed)

        except:
            only_arrow_post = True
            arrow_post = request.POST['arrow_post']
            if arrow_post == "up":
                arrow = "down"
            else:
                arrow = "up"
            try:
                if request.POST['avail'].find("disabled") > 0:
                    region_filter = True
                    button_pressed = last_pressed
                else:
                    region_filter = False
            except:
                pass

        if request.POST['avail'].find("disabled") > 0 and double_pressed != True:
            region_filter = True

        if only_arrow_post:
            button_pressed = last_pressed

        if button_pressed == "Release Date":
            if arrow == "up":
                imdb_Top_Tv = imdbTopTv.objects.all().order_by('release_date')
            else:
                imdb_Top_Tv = imdbTopTv.objects.all().order_by('-release_date')

        if button_pressed == "List Rank":
            if arrow == "up":
                imdb_Top_Tv = imdbTopTv.objects.all().order_by('rank')
            else:
                imdb_Top_Tv = imdbTopTv.objects.all().order_by('-rank')

        if button_pressed == "IMDB Rating":
            if arrow == "up":
                imdb_Top_Tv = imdbTopTv.objects.all().order_by('imdb_rating')
            else:
                imdb_Top_Tv = imdbTopTv.objects.all().order_by('-imdb_rating')

        if region_filter:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            if ip == "127.0.0.1":
                ip = "72.255.7.40"
            country = GeoIP2().city(ip)['country_name']

            if country == "Pakistan":
                country = "India"

            print(country)
            imdb_Top_Tv = imdbTopTv.objects.all().order_by('rank')
            wanted_items = set()
            not_wanted_items = set()
            for models in imdb_Top_Tv:
                if models.country.find(country) >= 0:
                    wanted_items.add(models.pk)
                else:
                    not_wanted_items.add(models.pk)

            if button_pressed == "Release Date":
                if arrow == "up":
                    imdb_Top_Tv = imdbTopTv.objects.filter(pk__in=wanted_items).order_by('release_date')
                else:
                    imdb_Top_Tv = imdbTopTv.objects.filter(pk__in=wanted_items).order_by('-release_date')

            if button_pressed == "List Rank":
                if arrow == "up":
                    imdb_Top_Tv = imdbTopTv.objects.filter(pk__in=wanted_items).order_by('rank')
                else:
                    imdb_Top_Tv = imdbTopTv.objects.filter(pk__in=wanted_items).order_by('-rank')

            if button_pressed == "IMDB Rating":
                if arrow == "up":
                    imdb_Top_Tv = imdbTopTv.objects.filter(pk__in=wanted_items).order_by('imdb_rating')
                else:
                    imdb_Top_Tv = imdbTopTv.objects.filter(pk__in=wanted_items).order_by('-imdb_rating')

    stuff_for_frontend = {
        'imdb_Top_Tv': imdb_Top_Tv,
        'nbar': 'topm',
        'arrow_pos': arrow,
        'button_disabled': button_pressed,
        'country': country,
        'region_filter': region_filter,

    }

    return render(request, 'toptv.html', stuff_for_frontend)
