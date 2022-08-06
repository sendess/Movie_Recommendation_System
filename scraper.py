import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import tqdm
import sklearn


"""
    Works for imdb pages recommend using all the pages with genres informations 
    discards all the ones wiht less then 3 genre type
"""

# 5 different genre 5 different pages scraping
# K means clustering



def get_all_titles(soup):
    result_topics = []
    all_topics = soup.find_all('h3', {'class': 'lister-item-header'})

    # print(all_topics)
    for topic in all_topics:

        topic = topic.find('a').text

        # topic = str(topic.find('a'))
        # topic = topic.replace('<', '=')
        # topic = topic.replace('>', '=')
        # topic = topic.split('=')
        # topic = topic[int(len(topic)/2)]
        result_topics.append(topic)

    # print(result_topics)
    return result_topics

def get_all_genres(soup):
    result_genre = []
    all_genre = soup.find_all('p', {"class": 'text-muted'})
    # print(all_genre)

    for genre in all_genre:
        genre = str(genre.find_all('span', {'class': 'genre'}))
        if genre == '[]':
            pass
        else:
            genre = genre.replace('<', '=')
            genre = genre.replace('>', '=')
            genre = genre.split('=')
            genre = genre[int(len(genre)/2)]
            result_genre.append(genre)

    return result_genre



def post_process(genres):
    post_process_genre = []
    for i in genres:
        i = i.replace('\n', '')
        i = i.replace(' ', '')
        post_process_genre.append(i)
    return post_process_genre


def check_repeated_comma(x):
    list_x = x.split(',')
    if len(list_x) == 3:
        return x
    else:
        return np.nan


def data_set(url):

    data_set = pd.DataFrame(columns = ["Movies", "Primary_Genre", "Secondary_Genre", "Tertiary_Genre"])

    # Initially get the page from the url and from the content extract all the things properly so page is extracetd
    page = requests.get(url)
    # Soup is created where all the content is parsed as html format so it can be extracted as seen in webpages. 
    soup = BeautifulSoup(page.content, 'html.parser')

    
    title = get_all_titles(soup)
    genres = get_all_genres(soup)
    genres = post_process(genres)

    data_set["Movies"] = pd.Series(title)
    data_set["Primary_Genre"] = pd.Series(genres)
    data_set["Primary_Genre"] = data_set["Primary_Genre"].apply(check_repeated_comma)
    data_set["Secondary_Genre"] = data_set["Secondary_Genre"].fillna('To be filled')
    data_set["Tertiary_Genre"] = data_set["Tertiary_Genre"].fillna('To be filled')

    data_set = data_set.loc[data_set["Primary_Genre"] != np.NaN]
    data_set = data_set.dropna(how = 'any')

    data_set[["Primary_Genre", "Secondary_Genre", "Tertiary_Genre"]] = data_set['Primary_Genre'].str.split(',', expand=True)

    data_set.to_csv('Dataset.csv', mode = 'a', header=False, index=False)


if __name__ == "__main__":
    import os
    os.system('cls')
    print('IMDB Scraper')
    number_of_genre = int(input("Enter numbers of genre you would like to scrape(<6): "))
    number_of_pages = int(input('Enter the pages for that genre to scrap(<6): '))


    # for i in range(number_of_pages):
    #     url = input('Enter a URL: ')
    #     data_set(url)


    genre_list = ['action', 'adventure', 'comedy', 'horror', 'thriller', 'darama']


    for i in tqdm.tqdm(range(number_of_genre)):
        count = 1
        for j in range(number_of_pages):
            url = f'https://www.imdb.com/search/title/?title_type=feature&genres={genre_list[i]}&start={count}&ref_=adv_nxt'
            count = count + 50
            print(url)
            data_set(url)