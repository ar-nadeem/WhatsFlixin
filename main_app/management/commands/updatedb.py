from django.core.management.base import BaseCommand
from main_app.models import imdbPopularMovie, imdbTopMovie
import requests, re
from bs4 import BeautifulSoup

base_url = "https://www.imdb.com"
imdb_pop_url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"
top_movie_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
netflix_search = "https://www.flixwatch.co/?s="
rotten_search = "https://www.rottentomatoes.com/search?search="

movie_titles = []
movie_urls = []
movie_descs = []
movie_ratings_imdb = []
movie_img_url = []
movie_poster = []
movie_netflix_url = []


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
        title = title[:title.find("(") - 1]

    title_searchable = (re.sub("[ ]", "+", title))
    response = requests.get(netflix_search + title_searchable)
    print(netflix_search + title_searchable)
    data = response.text

    soup = BeautifulSoup(data, features="lxml")
    check = soup.find_all('a', {'class': '_blank cvplbd'})

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

                    print("URL = " + check.get("href"))
                    movie_netflix_url.append(check.get("href"))
                except:
                    print("Error occurred setting URL to placeholder '/#' ")
                    movie_netflix_url.append(check.get("/#"))
                return found

        check = soup.find_all('a', {'class': '_blank cvplbd'})
        for check in check:
            print("FOUND using method 2")
            response = requests.get(check.get("href"))
            data = response.text

            soup = BeautifulSoup(data, features="lxml")
            check = soup.find('a', {'id': 'Netflix'})

            print("URL = " + check.get("href"))
            movie_netflix_url.append(check.get("href"))
            return found

    print("NOT FOUND")
    return found


def updatedb_popmovies():
    print("Updating DB for Popular Movies")
    delet = imdbPopularMovie.objects.all()

    # Get HTML from Popular Movie index on IMDB
    response = requests.get(imdb_pop_url)
    data = response.text
    soup = BeautifulSoup(data, features="lxml")
    movies = soup.find_all('td', {'class': 'posterColumn'})

    print("Scraping IMDB POPULAR MOVIES Urls to work from")

    # Scrape URLs of all the titles
    for movies in movies:
        a = ((movies.find('a')))
        movie_urls.append(base_url + (a['href']))

    # Loops through all the scraped URLs
    movie_rank = 0
    for urls in movie_urls:
        movie_rank = movie_rank + 1

        # Getting html from the URLs
        response = requests.get(urls)
        data = response.text
        soup = BeautifulSoup(data, features="lxml")

        # Getting Title
        title = soup.find('h1', class_="")
        try:
            title = title.text.strip()
        except AttributeError:
            print("Title is long finding by another logic")
            title = soup.find('h1', class_="long")
            title = title.text.strip()

        # Checking if title exists on Netflix
        print("Checking " + title)
        if check_on_netflix(title) == False:
            continue  # If not found skips the loop for this title
        movie_titles.append(title)

        # Getting Description
        desc = soup.find('div', class_="summary_text")
        movie_descs.append(desc.text.strip())

        # Getting Rating
        rating = soup.find('span', {'itemprop': 'ratingValue'})
        if rating != None:
            rating = (rating.text.strip()) + "/10"

        else:
            rating = "N/A"  # If Rating is not found (For unreleased titles)
        movie_ratings_imdb.append(rating)

        # Getting Poster
        image = soup.find('div', {'class': 'poster'})
        image = image.find('img').attrs['src']
        image = image[:(image.find("V1_")) + 3] + "SY1000_CR0,0,675,1000_AL_.jpg"
        movie_img_url.append(image)

        # For Testing purposes stop scraping after nth movie rank
        # if movie_rank > 5:
        #     break

    delet.delete()  # Deleting Previous DB to save space

    # Refilling models with the new scraped data
    for x in range(0, len(movie_titles)):
        movie_poster.append((x + 1, movie_titles[x], movie_descs[x], movie_ratings_imdb[x], movie_img_url[x],
                             movie_urls[x]))
        imdbPopularMovie.objects.create(poster_link=movie_img_url[x], title=movie_titles[x],
                                        description=movie_descs[x],
                                        rank=x + 1, imdb_rating=movie_ratings_imdb[x], netflix_url=movie_netflix_url[x])
    print("DB UPDATED")


def updatedb_topmovies():
    print("Updating DB for Top Rated Movies")
    delet = imdbTopMovie.objects.all()

    # Get HTML from Popular Movie index on IMDB
    response = requests.get(top_movie_url)
    data = response.text
    soup = BeautifulSoup(data, features="lxml")
    Pmovies = soup.find_all('td', {'class': 'posterColumn'})

    print("Scraping IMDB TOP-RATED MOVIES Urls to work from")

    # Scrape URLs of all the titles
    for Pmovies in Pmovies:
        a = ((Pmovies.find('a')))
        movie_urls.append(base_url + (a['href']))

    # Loops through all the scraped URLs
    movie_rank = 0
    for urls in movie_urls:
        movie_rank = movie_rank + 1

        # Getting html from the URLs
        response = requests.get(urls)
        data = response.text
        soup = BeautifulSoup(data, features="lxml")

        # Getting Title
        title = soup.find('h1', class_="")
        try:
            title = title.text.strip()
        except AttributeError:
            print("Title is long finding by another logic")
            title = soup.find('h1', class_="long")
            title = title.text.strip()

        # Checking if title exists on Netflix
        print("Checking " + title)
        if check_on_netflix(title) == False:
            continue  # If not found skips the loop for this title
        movie_titles.append(title)

        # Getting Description
        desc = soup.find('div', class_="summary_text")
        movie_descs.append(desc.text.strip())

        # Getting Rating
        rating = soup.find('span', {'itemprop': 'ratingValue'})
        if rating != None:
            rating = (rating.text.strip()) + "/10"

        else:
            rating = "N/A"  # If Rating is not found (For unreleased titles)
        movie_ratings_imdb.append(rating)

        # Getting Poster
        image = soup.find('div', {'class': 'poster'})
        image = image.find('img').attrs['src']
        image = image[:(image.find("V1_")) + 3] + "SY1000_CR0,0,675,1000_AL_.jpg"
        movie_img_url.append(image)

        # For Testing purposes stop scraping after nth movie rank
        # if movie_rank > 5:
        #     break

    delet.delete()  # Deleting Previous DB to save space

    # Refilling models with the new scraped data
    for x in range(0, len(movie_titles)):
        movie_poster.append((x + 1, movie_titles[x], movie_descs[x], movie_ratings_imdb[x], movie_img_url[x],
                             movie_urls[x]))
        imdbTopMovie.objects.create(poster_link=movie_img_url[x], title=movie_titles[x],
                                    description=movie_descs[x],
                                    rank=x + 1, imdb_rating=movie_ratings_imdb[x], netflix_url=movie_netflix_url[x])
    print("DB UPDATED")


# Logic for Management Command
class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("arg", type=str)

    def handle(self, **options):
        if options['arg'] == "popm":  # Update IMDB Popular Movie Index
            updatedb_popmovies()
        elif options['arg'] == "topm":  # Update IMDB Top Movie Index
            updatedb_topmovies()
        elif options['arg'] == "test":  # For testing purposes
            # title = input("Enter movie title : ")
            check_on_netflix("The Shawshank Redemption")

# Bismillah Alhumdilillah
