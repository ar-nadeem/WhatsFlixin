from django.core.management.base import BaseCommand, CommandError
from main_app.models import imdbPopMovie, imdbTopMovie, imdbPopTv, imdbTopTv
import requests, re, time, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Pesonal Debuging Key
# ombdAPI="1d54010c"

#Official WhatsFlixin Key
ombdAPI="c8d38112"


rotten_rate=[]
meta_rate =[]
y_trailer_url=[]
from selenium.common.exceptions import NoSuchElementException
base_url = "https://www.imdb.com"
pop_movie_url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"
top_movie_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
pop_tv_url = "https://www.imdb.com/chart/tvmeter/?ref_=nv_tvv_mptv"
top_tv_url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"
# netflix_search = "https://www.flixwatch.co/?s="
rotten_search = "https://www.rottentomatoes.com/search?search="
netflix_search = "https://unogs.com/search/{}?start_year={}&end_year={}&end_rating=10&orderby=Relevance" # removed &type=Movie from the url to carter for TVs

movie_rank = 0
movie_titles = []
movie_urls = []
movie_descs = []
movie_ratings_imdb = []
movie_img_url = []
movie_poster = []
movie_netflix_url = []
movie_country = []
tv_rel_date = []



print("WAITING FOR TOR TO FULLY LOAD - 10 sec")
time.sleep(10)
######################### HEROKU  ################################
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
PROXY = "socks5://127.0.0.1:9050"
chrome_options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

##################### LOCAL #######################
# chrome_options = Options()
# # chrome_options.add_argument("--headless")
# PROXY = "socks5://127.0.0.1:9150"
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
# driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)


timeout = 60
wait = WebDriverWait(driver, 60)


def check_on_netflix(title):
    found = False
    date_found = True
    title_searchable = "THIS IS A PLACEHOLDER -- SOMETHING WENT WRONG IF YOU SEE THIS"
    if title.find("(") != -1:
        title_searchable = title[:title.find("(") - 1]
    else:
        date_found = False
        title_searchable = title
    #   Adding an exception for a popular movie

    if title_searchable == "Once Upon a Time... in Hollywood":
        title_searchable = "Once Upon a Time in Hollywood"
    if title_searchable == "Whose Line Is It Anyway?":
        return found
    if date_found == True:
        if title_searchable.find("/") != -1:
            title_searchable = title_searchable[:title_searchable.find("/")]

    #   Setting up the search URL
    title_searchable_formated = (re.sub("[ ]", "%20", title_searchable))
    if date_found == True:
        year = title[title.find("(") + 1:title.find(")")]
    else:
        year=""

    netflix_search_formatted = netflix_search.format(title_searchable_formated, year, year)

    #   Get URL and wait for load
    driver.get(netflix_search_formatted)
    element_present = EC.presence_of_element_located((By.XPATH, """/html/body/div[9]/div[1]/div/div/div"""))
    WebDriverWait(driver, timeout).until(element_present)

    # time.sleep(0.5)

    #   Checking if there are results
    if (len(driver.find_elements_by_class_name("titleitem"))) == 0:
        print("Not Found")
        return found  # Result not found just return bol found
    else:
        driver.find_elements_by_class_name("titleitem")
        print("Searched -- Fetching INFO")

    #   Getting page HTML and sending it to BS4 for scraping
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    check = soup.find_all(attrs={"data-bind": "html:title"})  # Title of the movie
    print(title_searchable)
    # Looping Through until found
    for check in check:
        if check.text == title_searchable:
            found = True

            driver.find_elements_by_class_name("titleitem")[0].click()  # If found Click the title to bring up overlay

            # Waiting for the page to load
            try:
                element_present = EC.presence_of_element_located(
                    (By.XPATH, """//*[@id="titleDetails"]/div/div/div[3]/div[3]/div[5]/div[3]"""))
                WebDriverWait(driver, timeout).until(element_present)
                # print("\nPage Ready\n")

                # Getting HTML to send to BS4
                html = driver.page_source
                soup = BeautifulSoup(html, features="lxml")
                check = soup.find(attrs={"data-bind": "attr:{href:netflixpath}"})

                if title_searchable == "Dark":
                    movie_netflix_url.append("https://www.netflix.com/title/80100172")
                else:
                    movie_netflix_url.append(check['href'])  # Netflix Stream Link to that title

                # Getting Countries for that title
                check = soup.find_all(attrs={"data-bind": "html:country"})

                # Setting country_appended Back to null string
                country_appended = ""
                for check in check:  # Loop to go through all countries (Taken care to make sure countries are only seprated by commas)
                    if check.text[len(check.text) - 1:] == " ":
                        country_appended += check.text[:len(check.text) - 1] + ","
                    else:
                        country_appended += check.text + ","

                movie_country.append(country_appended[:len(country_appended) - 1])  # remove last comma and append

                # All the Info fetched and returned found

                return found




            except TimeoutException:  # Page not loaded SO returning not found
                print("Loading took too much time!")
                print("NOT FOUND")
                return found

    print("THE INFO FOR TITLE WAS NOT FOUND")
    return found


def updatedb_popmovies():
    global driver
    print("Updating DB for Popular Movies")
    delet = imdbPopMovie.objects.all()

    # Get HTML from Popular Movie index on IMDB
    response = requests.get(pop_movie_url)
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
        print("Found info Fetched")

        # Getting Description
        desc = soup.find('div', class_="summary_text")
        movie_descs.append(desc.text.strip())

        # Getting Rating IMDB
        rating = soup.find('span', {'itemprop': 'ratingValue'})
        if rating != None:
            rating = (rating.text.strip()) + "/10"
        else:
            rating = "N/A"  # If Rating is not found (For unreleased titles)
        movie_ratings_imdb.append(rating)

        # Getting OMBD DATA
        omdb = requests.get("http://www.omdbapi.com/?i="+(urls[urls.find("/tt")+1:urls.find("?")])+"&y=&plot=short&tomatoes=true&r=json&apikey="+ombdAPI).json()

        # Getting Rotten Rating
        rotten_rate.append(omdb["tomatoRotten"])
        # Getting Meta Rating
        meta_rate.append(omdb["Metascore"])

        # Getting Poster
        image = soup.find('div', {'class': 'poster'})
        image = image.find('img').attrs['src']
        image = image[:(image.find("V1_")) + 3] + "SY1000_CR0,0,675,1000_AL_.jpg"
        movie_img_url.append(image)

        # Getting Trailer LINK
        youtube = requests.get("https://www.youtube.com/results?search_query="+(re.sub("[ ]", "%20", title))+"%20Trailer")
        y_part_1 = youtube.text[(youtube.text.find("/watch?v="))+9:]
        trailer_url_raw =  y_part_1[:y_part_1.find('"')]
        y_trailer_url.append("https://www.youtube.com/embed/"+trailer_url_raw)

        # For Testing purposes stop scraping after nth movie rank
        # if movie_rank > 10:
        #     print("DONE EXITING AT 10")
        #     driver.quit()
        #     break

    delet.delete()  # Deleting Previous DB to save space

    # Refilling models with the new scraped data
    for x in range(0, len(movie_titles)):
        # movie_poster.append((x + 1, movie_titles[x], movie_descs[x], movie_ratings_imdb[x], movie_img_url[x],
        #                      movie_urls[x]))
        imdbPopMovie.objects.create(poster_link=movie_img_url[x], title=movie_titles[x],
                                    description=movie_descs[x],
                                    rank=x + 1, imdb_rating=movie_ratings_imdb[x], netflix_url=movie_netflix_url[x],
                                    country=movie_country[x],release_date=(movie_titles[x][movie_titles[x].find("(")+1:movie_titles[x].find(")")]),
                                    rotten_rating=rotten_rate[x],meta_rating=meta_rate[x],trailer_url=y_trailer_url[x])
    print("DB UPDATED")


def updatedb_topmovies():
    global driver
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
        print("Found info Fetched")

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

        # Getting OMBD DATA
        omdb = requests.get("http://www.omdbapi.com/?i="+(urls[urls.find("/tt")+1:urls.find("?")])+"&y=&plot=short&tomatoes=true&r=json&apikey="+ombdAPI).json()

        # Getting Rotten Rating
        rotten_rate.append(omdb["tomatoRotten"])
        # Getting Meta Rating
        meta_rate.append(omdb["Metascore"])


        # Getting Poster
        image = soup.find('div', {'class': 'poster'})
        image = image.find('img').attrs['src']
        image = image[:(image.find("V1_")) + 3] + "SY1000_CR0,0,675,1000_AL_.jpg"
        movie_img_url.append(image)

        # Getting Trailer LINK
        youtube = requests.get("https://www.youtube.com/results?search_query="+(re.sub("[ ]", "%20", title))+"%20Trailer")
        y_part_1 = youtube.text[(youtube.text.find("/watch?v="))+9:]
        trailer_url_raw =  y_part_1[:y_part_1.find('"')]
        y_trailer_url.append("https://www.youtube.com/embed/"+trailer_url_raw)



        # For Testing purposes stop scraping after nth movie rank
        # if movie_rank > 10:
        #     print("DONE EXITING AT 10")
        #     driver.quit()
        #     break

    delet.delete()  # Deleting Previous DB to save space

    # Refilling models with the new scraped data
    for x in range(0, len(movie_titles)):
        # movie_poster.append((x + 1, movie_titles[x], movie_descs[x], movie_ratings_imdb[x], movie_img_url[x],
        #                      movie_urls[x]))
        imdbTopMovie.objects.create(poster_link=movie_img_url[x], title=movie_titles[x],
                                    description=movie_descs[x],
                                    rank=x + 1, imdb_rating=movie_ratings_imdb[x], netflix_url=movie_netflix_url[x],
                                    country=movie_country[x],release_date=(movie_titles[x][movie_titles[x].find("(")+1:movie_titles[x].find(")")]),
                                    rotten_rating=rotten_rate[x],meta_rating=meta_rate[x],trailer_url=y_trailer_url[x])
    print("DB UPDATED")


def updatedb_toptv():
    global driver
    print("Updating DB for Top Rated TV")
    delet = imdbTopTv.objects.all()

    # Get HTML from Popular Movie index on IMDB
    response = requests.get(top_tv_url)
    data = response.text
    soup = BeautifulSoup(data, features="lxml")
    Pmovies = soup.find_all('td', {'class': 'posterColumn'})

    print("Scraping IMDB TOP-RATED TV Urls to work from")

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

            # Special Method for TVs only Adds (2008)  Year to the title
            date = soup.find('a', title="See more release dates")
            date_for_display = (date.text.strip()[date.text.strip().find("("):date.text.strip().find(")")+1])
            date_for_search = date.text.strip()[date.text.strip().find("("):date.text.strip().find("–")]
            if (date_for_search[len(date_for_search) - 1:]) != ")":
                date_for_search += ")"





        except AttributeError:
            print("Title is long finding by another logic")
            title = soup.find('h1', class_="long")
            title = title.text.strip()

        # Checking if title exists on Netflix
        print("Checking " + title)
        if check_on_netflix(title+" "+date_for_search) == False:
            continue  # If not found skips the loop for this title
        movie_titles.append(title+" "+date_for_display)
        print("Found info Fetched")
        tv_rel_date.append(date_for_search)
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

        # Getting OMBD DATA
        omdb = requests.get("http://www.omdbapi.com/?i="+(urls[urls.find("/tt")+1:urls.find("?")])+"&y=&plot=short&tomatoes=true&r=json&apikey="+ombdAPI).json()

        # Getting Rotten Rating
        rotten_rate.append(omdb["tomatoRotten"])
        # Getting Meta Rating
        meta_rate.append(omdb["Metascore"])


        # Getting Poster
        image = soup.find('div', {'class': 'poster'})
        image = image.find('img').attrs['src']
        image = image[:(image.find("V1_")) + 3] + "SY1000_CR0,0,675,1000_AL_.jpg"
        movie_img_url.append(image)

        # Getting Trailer LINK
        youtube_search = title+" "+date_for_search
        youtube = requests.get("https://www.youtube.com/results?search_query="+(re.sub("[ ]", "%20", youtube_search)+"%20Trailer"))
        y_part_1 = youtube.text[(youtube.text.find("/watch?v="))+9:]
        trailer_url_raw =  y_part_1[:y_part_1.find('"')]
        y_trailer_url.append("https://www.youtube.com/embed/"+trailer_url_raw)

        # For Testing purposes stop scraping after nth movie rank
        # if movie_rank > 10:
        #     print("DONE EXITING AT 10")
        #     driver.quit()
        #     break


    delet.delete()  # Deleting Previous DB to save space

    # Refilling models with the new scraped data
    for x in range(0, len(movie_titles)):
        # movie_poster.append((x + 1, movie_titles[x], movie_descs[x], movie_ratings_imdb[x], movie_img_url[x],
        #                      movie_urls[x]))
        imdbTopTv.objects.create(poster_link=movie_img_url[x], title=movie_titles[x],
                                 description=movie_descs[x],
                                 rank=x + 1, imdb_rating=movie_ratings_imdb[x], netflix_url=movie_netflix_url[x],
                                 country=movie_country[x],release_date=(tv_rel_date[x][tv_rel_date[x].find("(")+1:tv_rel_date[x].find(")")]),
                                 rotten_rating=rotten_rate[x],meta_rating=meta_rate[x],trailer_url=y_trailer_url[x])
    print("DB UPDATED")

def updatedb_poptv():
    global driver
    print("Updating DB for Popular TV")
    delet = imdbPopTv.objects.all()

    # Get HTML from Popular Movie index on IMDB
    response = requests.get(pop_tv_url)
    data = response.text
    soup = BeautifulSoup(data, features="lxml")
    Pmovies = soup.find_all('td', {'class': 'posterColumn'})

    print("Scraping IMDB Popular TV Urls to work from")

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

            # Special Method for TVs only Adds (2008)  Year to the title
            date = soup.find('a', title="See more release dates")
            date_for_display = (date.text.strip()[date.text.strip().find("("):date.text.strip().find(")")+1])
            date_for_search = date.text.strip()[date.text.strip().find("("):date.text.strip().find("–")]
            if (date_for_search[len(date_for_search) - 1:]) != ")":
                date_for_search += ")"



        except AttributeError:
            print("Title is long finding by another logic")
            title = soup.find('h1', class_="long")
            title = title.text.strip()

        # Checking if title exists on Netflix
        print("Checking " + title)
        if check_on_netflix(title+" "+date_for_search) == False:
            continue  # If not found skips the loop for this title
        movie_titles.append(title+" "+date_for_display)
        print("Found info Fetched")
        tv_rel_date.append(date_for_search)

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

        # Getting OMBD DATA
        omdb = requests.get("http://www.omdbapi.com/?i="+(urls[urls.find("/tt")+1:urls.find("?")])+"&y=&plot=short&tomatoes=true&r=json&apikey="+ombdAPI).json()

        # Getting Rotten Rating
        rotten_rate.append(omdb["tomatoRotten"])
        # Getting Meta Rating
        meta_rate.append(omdb["Metascore"])

        # Getting Poster
        image = soup.find('div', {'class': 'poster'})
        image = image.find('img').attrs['src']
        image = image[:(image.find("V1_")) + 3] + "SY1000_CR0,0,675,1000_AL_.jpg"
        movie_img_url.append(image)

        # Getting Trailer LINK
        youtube_search = title+" "+date_for_search
        youtube = requests.get("https://www.youtube.com/results?search_query="+(re.sub("[ ]", "%20", youtube_search)+"%20Trailer"))
        y_part_1 = youtube.text[(youtube.text.find("/watch?v="))+9:]
        trailer_url_raw =  y_part_1[:y_part_1.find('"')]
        y_trailer_url.append("https://www.youtube.com/embed/"+trailer_url_raw)

        # For Testing purposes stop scraping after nth movie rank
        # if movie_rank > 10:
        #     print("DONE EXITING AT 10")
        #     driver.quit()
        #     break


    delet.delete()  # Deleting Previous DB to save space

    # Refilling models with the new scraped data
    for x in range(0, len(movie_titles)):
        # movie_poster.append((x + 1, movie_titles[x], movie_descs[x], movie_ratings_imdb[x], movie_img_url[x],
        #                      movie_urls[x]))
        imdbPopTv.objects.create(poster_link=movie_img_url[x], title=movie_titles[x],
                                 description=movie_descs[x],
                                 rank=x + 1, imdb_rating=movie_ratings_imdb[x], netflix_url=movie_netflix_url[x],
                                 country=movie_country[x],release_date=(tv_rel_date[x][tv_rel_date[x].find("(")+1:tv_rel_date[x].find(")")]),
                                 rotten_rating=rotten_rate[x],meta_rating=meta_rate[x],trailer_url=y_trailer_url[x])
    print("DB UPDATED")


def clear_all_variables():
    movie_rank = 0
    movie_titles = []
    movie_urls = []
    movie_descs = []
    movie_ratings_imdb = []
    movie_img_url = []
    movie_poster = []
    movie_netflix_url = []
    movie_country = []
    tv_rel_date = []




# Logic for Management Command
class Command(BaseCommand):
    help = "Updates Database and shit"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('arg', type=str)

    def handle(self, *args, **options):
        if options['arg'] == "popm":  # Update IMDB Popular Movie Index
            updatedb_popmovies()
            clear_all_variables()
            driver.quit()
            print("DONE EVERYTHING ENDED SUCCESSFULLY")
        elif options['arg'] == "topm":  # Update IMDB Top Movie Index
            updatedb_topmovies()
            clear_all_variables()
            driver.quit()
            print("DONE EVERYTHING ENDED SUCCESSFULLY")
        elif options['arg'] == "poptv":  # Update IMDB Top Movie Index
            updatedb_poptv()
            clear_all_variables()
            driver.quit()
            print("DONE EVERYTHING ENDED SUCCESSFULLY")
        elif options['arg'] == "toptv":  # Update IMDB Top Movie Index
            updatedb_toptv()
            clear_all_variables()
            driver.quit()
            print("DONE EVERYTHING ENDED SUCCESSFULLY")
        elif options['arg'] == "test":  # For testing purposes
            # title = input("Enter movie title : ")
            check_on_netflix("Da 5 Bloods (2020)")
            driver.quit()


# Bismillah Alhumdilillah
