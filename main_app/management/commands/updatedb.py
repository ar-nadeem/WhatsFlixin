from django.core.management.base import BaseCommand
from main_app.models import imdbPopularMovie, imdbTopMovie
import requests, re, time, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


base_url = "https://www.imdb.com"
imdb_pop_url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"
top_movie_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
# netflix_search = "https://www.flixwatch.co/?s="
rotten_search = "https://www.rottentomatoes.com/search?search="
netflix_search = "https://unogs.com/search/{}?start_year={}&end_year={}&end_rating=10&type=Movie&orderby=Relevance"

movie_titles = []
movie_urls = []
movie_descs = []
movie_ratings_imdb = []
movie_img_url = []
movie_poster = []
movie_netflix_url = []
movie_country = ""

######################### HEROKU  ################################
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


##################### LOCAL #######################
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(chrome_options=chrome_options)



timeout = 10
wait = WebDriverWait(driver, 10)


def check_on_netflix(title):
    found = False
    if title.find("(") != -1:
        title_searchable = title[:title.find("(") - 1]
    #   Adding an exception for a popular movie
    if title_searchable == "Once Upon a Time... in Hollywood":
        title_searchable = "Once Upon a Time in Hollywood"

    #   Setting up the search URL
    title_searchable_formated = (re.sub("[ ]", "%20", title_searchable))
    year = title[title.find("(") + 1:title.find(")")]
    netflix_search_formatted = netflix_search.format(title_searchable_formated, year, year)

    #   Get URL and wait for load
    driver.get(netflix_search_formatted)
    element_present = EC.presence_of_element_located((By.XPATH, """/html/body/div[9]/div[1]/div/div/div"""))
    WebDriverWait(driver, timeout).until(element_present)

    #time.sleep(0.5)

    #   Checking if there are results
    if (len(driver.find_elements_by_class_name("titleitem"))) == 0:
        print("Not Found")
        return found    #   Result not found just return bol found
    else:
        driver.find_elements_by_class_name("titleitem")
        print("FOUND -- Fetching INFO")


    #   Getting page HTML and sending it to BS4 for scraping
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    check = soup.find_all(attrs={"data-bind": "html:title"})    #Title of the movie

    #Looping Through until found
    for check in check:
        if check.text == title_searchable:
            found = True

            driver.find_elements_by_class_name("titleitem")[0].click()  # If found Click the title to bring up overlay

            #Waiting for the page to load
            try:
                element_present = EC.presence_of_element_located((By.XPATH, """//*[@id="titleDetails"]/div/div/div[3]/div[3]/div[5]/div[3]"""))
                WebDriverWait(driver, timeout).until(element_present)
                #print("\nPage Ready\n")

                # Getting HTML to send to BS4
                html = driver.page_source
                soup = BeautifulSoup(html, features="lxml")
                check = soup.find(attrs={"data-bind": "attr:{href:netflixpath}"})
                movie_netflix_url.append(check['href'])    # Netflix Stream Link to that title


                # Getting Countries for that title
                check = soup.find_all(attrs={"data-bind": "html:country"})
                movie_country = ""  # Delete the previous list

                for check in check:     # Loop to go through all countries (Taken care to make sure countries are only seprated by commas)
                    if check.text[len(check.text) - 1:] == " ":
                        country = check.text[:len(check.text) - 1]
                    else:
                        country = check.text
                    movie_country +=  country + ","
                movie_country = movie_country[:len(movie_country) - 1]  # remove last comma


                # All the Info fetched and returned found

                return found




            except TimeoutException: # Page not loaded SO returning not found
                print("Loading took too much time!")
                print("NOT FOUND")
                return found



    print("THE IF FOR TITLE WAS NOT FOUND")
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
                                        rank=x + 1, imdb_rating=movie_ratings_imdb[x], netflix_url=movie_netflix_url[x], country=movie_country)
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

        # Getting Poster
        image = soup.find('div', {'class': 'poster'})
        image = image.find('img').attrs['src']
        image = image[:(image.find("V1_")) + 3] + "SY1000_CR0,0,675,1000_AL_.jpg"
        movie_img_url.append(image)

        #For Testing purposes stop scraping after nth movie rank
        # if movie_rank > 5:
        #     driver.quit()
        #     break

    delet.delete()  # Deleting Previous DB to save space

    # Refilling models with the new scraped data
    for x in range(0, len(movie_titles)):
        movie_poster.append((x + 1, movie_titles[x], movie_descs[x], movie_ratings_imdb[x], movie_img_url[x],
                             movie_urls[x]))
        imdbTopMovie.objects.create(poster_link=movie_img_url[x], title=movie_titles[x],
                                    description=movie_descs[x],
                                    rank=x + 1, imdb_rating=movie_ratings_imdb[x], netflix_url=movie_netflix_url[x], country=movie_country)
    print("DB UPDATED")


# Logic for Management Command
class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("arg", type=str)

    def handle(self, **options):
        if options['arg'] == "popm":  # Update IMDB Popular Movie Index
            updatedb_popmovies()
            driver.quit()
        elif options['arg'] == "topm":  # Update IMDB Top Movie Index
            updatedb_topmovies()
            driver.quit()
        elif options['arg'] == "test":  # For testing purposes
            # title = input("Enter movie title : ")
            check_on_netflix("Da 5 Bloods (2020)")
            driver.quit()


# Bismillah Alhumdilillah
