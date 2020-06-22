from django.core.management.base import BaseCommand, CommandError
from main_app.models import PopularMovie, TopMovie
import requests
import re
from bs4 import BeautifulSoup

base_url = "https://www.imdb.com"
pop_movie_url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"
top_movie_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
netflix_search = "https://www.flixwatch.co/?s="
rotten_search = "https://www.rottentomatoes.com/search?search="

Pmovie_titles = []
Pmovie_urls = []
Pmovie_descs = []
Pmovie_ratings = []
Pmovie_img_url = []
Pmovie_post = []
Pmovie_netflix_url=[]

def rotten_rating(title):
    pass

    # found = False
    # if title.find("(") != -1:
    #     title = title[:title.find("(") - 1]
    #
    # result = RottenTomatoesClient.browse_movies(query=title)
    # print(result)

    # title_searchable = (re.sub("[ ]", "%20", title))
    #
    # response = requests.get(rotten_search + title_searchable)
    # data = response.text
    #
    # soup = BeautifulSoup(data, features="lxml")
    # check = soup.find_all('script', {'id': 'movies-json'})
    #
    # new_url = str(check[0])
    # new_url = new_url[new_url.find('"url":"')+7:]
    # new_url = new_url[:new_url.find('"')]
    #
    # response = requests.get(new_url)
    # data = response.text
    #
    # soup = BeautifulSoup(data, features="lxml")
    # check = soup.find_all('span', {'id': 'mop-ratings-wrap__percentage'})
    # print (soup.prettify())





def check_on_netflix(title):
    found = False
    if title.find("(") != -1:
        title = title[:title.find("(")-1]

    title_searchable = (re.sub("[ ]", "+", title))
    response = requests.get(netflix_search+title_searchable)
    print(netflix_search+title_searchable)
    data = response.text

    soup = BeautifulSoup(data, features="lxml")
    check = soup.find_all('a',{'class':'_blank cvplbd'})

    if len(check) >= 1:
        found = True

        for check in check:

            if (title == check.text):

                print("FOUND Perfectly")
                # found = True
                print("Fetching Netflix Streaming URL for that title !")
                try:
                    response = requests.get(check.get("href"))
                    data = response.text

                    soup = BeautifulSoup(data, features="lxml")
                    check = soup.find('a', {'id': 'Netflix'})

                    print("URL = "+check.get("href"))
                    Pmovie_netflix_url.append(check.get("href"))
                except:
                    print("Error occurred setting URL to placeholder '/#' ")
                    Pmovie_netflix_url.append(check.get("/#"))
                return found

        check = soup.find_all('a', {'class': '_blank cvplbd'})
        for check in check:
            print("FOUND using method 2")
            response = requests.get(check.get("href"))
            data = response.text

            soup = BeautifulSoup(data, features="lxml")
            check = soup.find('a', {'id': 'Netflix'})

            print("URL = " + check.get("href"))
            Pmovie_netflix_url.append(check.get("href"))
            return found



    print("NOT FOUND")
    return found

def updatedb_popmovies():
    print("Updating DB for Popular Movies")
    delet = PopularMovie.objects.all()


    response = requests.get(pop_movie_url)
    data = response.text

    soup = BeautifulSoup(data, features="lxml")
    Pmovies = soup.find_all('td', {'class': 'posterColumn'})

    print ("Scraping IMDB POPULAR MOVIES Urls to work from")

    for Pmovies in Pmovies:
        a = ((Pmovies.find('a')))
        Pmovie_urls.append(base_url + (a['href']))

    x = 0
    for urls in Pmovie_urls:
        x = x + 1

        response = requests.get(urls)
        data = response.text
        soup = BeautifulSoup(data, features="lxml")

        title = soup.find('h1', class_="")
        try:
            title = title.text.strip()
        except AttributeError:
            print("Could'nt Get URL trying something else")
            title = soup.find('h1', class_="long")
            title = title.text.strip()


        print("Checking " + title)

        if check_on_netflix(title) == False:

            continue

        Pmovie_titles.append(title)

        desc = soup.find('div', class_="summary_text")
        Pmovie_descs.append(desc.text.strip())

        rating = soup.find('span', {'itemprop': 'ratingValue'})
        if rating != None:
            rating = (rating.text.strip()) + "/10"

        else:
            rating = "N/A"
        Pmovie_ratings.append(rating)

        image = soup.find('div', {'class': 'poster'})
        image = image.find('img').attrs['src']
        image = image[:(image.find("V1_")) + 3] + "SY1000_CR0,0,675,1000_AL_.jpg"
        Pmovie_img_url.append(image)

        # if x > 5:
        #     break

    delet.delete()
    for x in range(0, len(Pmovie_titles)):
        Pmovie_post.append((x + 1, Pmovie_titles[x], Pmovie_descs[x], Pmovie_ratings[x], Pmovie_img_url[x],
                            Pmovie_urls[x]))
        PopularMovie.objects.create(poster_link=Pmovie_img_url[x], title=Pmovie_titles[x],
                                    description=Pmovie_descs[x],
                                    rank=x + 1, rating=Pmovie_ratings[x], netflix_url=Pmovie_netflix_url[x])
    print("DB UPDATED")

def updatedb_topmovies():
    print("Updating DB for Top Rated Movies")
    delet = TopMovie.objects.all()


    response = requests.get(top_movie_url)
    data = response.text

    soup = BeautifulSoup(data, features="lxml")
    Pmovies = soup.find_all('td', {'class': 'posterColumn'})

    print("Scraping IMDB TOP-RATED MOVIES Urls to work from")

    for Pmovies in Pmovies:
        a = ((Pmovies.find('a')))
        Pmovie_urls.append(base_url + (a['href']))

    x = 0
    for urls in Pmovie_urls:
        x = x + 1

        response = requests.get(urls)
        data = response.text
        soup = BeautifulSoup(data, features="lxml")

        title = soup.find('h1', class_="")
        try:
            title = title.text.strip()
        except AttributeError:
            print("Could'nt Get URL trying something else")
            title = soup.find('h1', class_="long")
            title = title.text.strip()

        print("Checking " + title)

        if check_on_netflix(title) == False:

            continue

        Pmovie_titles.append(title)

        desc = soup.find('div', class_="summary_text")
        Pmovie_descs.append(desc.text.strip())

        rating = soup.find('span', {'itemprop': 'ratingValue'})
        if rating != None:
            rating = (rating.text.strip()) + "/10"

        else:
            rating = "N/A"
        Pmovie_ratings.append(rating)

        image = soup.find('div', {'class': 'poster'})
        image = image.find('img').attrs['src']
        image = image[:(image.find("V1_")) + 3] + "SY1000_CR0,0,675,1000_AL_.jpg"
        Pmovie_img_url.append(image)

        # if x > 5:
        #     break

    delet.delete()
    for x in range(0,len(Pmovie_titles)):
        Pmovie_post.append((x + 1, Pmovie_titles[x], Pmovie_descs[x], Pmovie_ratings[x], Pmovie_img_url[x],
                            Pmovie_urls[x]))
        TopMovie.objects.create(poster_link=Pmovie_img_url[x], title=Pmovie_titles[x],
                                    description=Pmovie_descs[x],
                                    rank=x + 1, rating=Pmovie_ratings[x], netflix_url=Pmovie_netflix_url[x])
    print("DB UPDATED")


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("arg", type=str)
        help = "popm -- Updates Popular Movies Database\n topm -- Updates Top Movies Database"


    def handle(self, **options):
        if options['arg'] == "popm" :
            updatedb_popmovies()
        elif options['arg'] == "topm" :
            updatedb_topmovies()
        elif options['arg'] == "test":
            #title = input("Enter movie title : ")
            check_on_netflix("The Shawshank Redemption")


# Bismillah Alhumdilillah