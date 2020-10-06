# -*- coding: utf-8 -*-

import logging
from film_crawler.items import FilmCrawlerItem
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider

actors_seen = []
actors_parsed = {}
films_seen = []
films_parsed = {}

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


# Exacts the int representation for the box office value
def format_box_office(payload):
    logging.info("Extracting Box Office Value for film")
    box_office = 0
    if "million" in payload:
        logging.debug("Using Million formatting")
        payload = payload.replace("$", "")
        index = payload.find("m")
        hypen_index = payload.find("-")
        if hypen_index != -1:
            box_office = float(payload[0:hypen_index].strip()) * 1000000
        else:
            box_office = float(payload[0:index].strip()) * 1000000
    elif "billion" in payload:
        logging.debug("Using Billion formatting")
        payload = payload.replace("$", "")
        payload.replace("billion", "")
        index = payload.find("b")
        hypen_index = payload.find("-")
        if hypen_index != -1:
            box_office = float(payload[0:hypen_index]) * 1000000000
        else:
            box_office = float(payload[0:index]) * 1000000000
    else:
        logging.debug("Film does not use the billion/million format!")
        payload = payload.replace("$", "")
        payload = payload.replace(",", "")
        index = payload.find("[")
        if index != -1:
            box_office = float(payload[0:index])
        else:
            box_office = float(payload)

    logging.debug("Film value is: " + str(box_office))
    return box_office


def extract_release_date(soup):
    release_date_info = soup.find("span", {"class": "bday dtstart published updated"})
    if release_date_info:
        release_date_info = release_date_info.text
        release_date_info = release_date_info[0:4]
        logging.debug("Release date is: " + release_date_info)
        return release_date_info
    return None


# General formatting function for extracting information about a film
# This includes: box_office value, and starring actors
def filter_film_info(soup):
    film_info = {}
    logging.info("Called film filter")
    data = []
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        heading = row.find('th')
        if heading:
            heading = heading.text.strip()
            if heading == "Box office":
                raw_string = columns[0].text.strip()
                box_office = format_box_office(raw_string)
                film_info["box_office"] = box_office
            if heading == "Starring":
                if columns:
                    cast_info = columns[0].find_all('a', href=True)
                    cast = []
                    for each in cast_info:
                        name = each.text.strip()
                        new_link = "https://en.wikipedia.org/" + str(each['href'])
                        logging.debug("Actor: " + name + " at link " + new_link)
                        cast.append(name)
                    if len(cast) > 0:
                        film_info['cast'] = cast
                        print(cast)
    if film_info:
        return film_info
    else:
        logging.warning("Film Filter returning with None Type!")
        return None


# This function extras the relevant info for an actor
def filter_actor_info(soup):
    birth_day = soup.find("span", {"class": "bday"})
    if birth_day:
        birth_day = birth_day.text.strip()
        birth_year = int(birth_day[0:4])
        actor_age = 2019 - birth_year
        return birth_year, actor_age
    logging.warning("Actor does not have a birthday!")
    return 0, 0


class PagesSpider(CrawlSpider):
    name = "film_wiki_spider"
    allowed_domains = ["wikipedia.org"]
    page_counter = 0

    start_urls = [
        "https://en.wikipedia.org/wiki/Matthew_McConaughey",
        "https://en.wikipedia.org/wiki/Morgan_Freeman",
        "https://en.wikipedia.org/wiki/Interstellar_(film)",
        "https://en.wikipedia.org/wiki/The_Shawshank_Redemption",
        "https://en.wikipedia.org/wiki/No_Country_for_Old_Men_(film)",
        "https://en.wikipedia.org/wiki/The_Wolf_of_Wall_Street_(2013_film)"
    ]

    rules = (
        Rule(LinkExtractor(allow="https://en\.wikipedia\.org/wiki/.+_.+",
                           deny=[
                               "https://en\.wikipedia\.org/wiki/Wikipedia.*",
                               "https://en\.wikipedia\.org/wiki/Main_Page",
                               "https://en\.wikipedia\.org/wiki/Free_Content",
                               "https://en\.wikipedia\.org/wiki/Talk.*",
                               "https://en\.wikipedia\.org/wiki/Portal.*",
                               "https://en\.wikipedia\.org/wiki/Special.*"
                           ]),
             callback='parse_film_page'),
    )

    def parse_film_page(self, response):
        if len(actors_seen) > 300 and len(films_seen) > 400:
            logging.critical("Stopping the SPIDER!")
            logging.critical("Actors: " + str(len(actors_seen)))
            logging.critical("Films: " + str(len(films_seen)))
            print('\a')
            print('\a')
            print('\a')
            print('\a')
            print('\a')
            raise CloseSpider('Search Exceeded 500')

        item = FilmCrawlerItem()
        soup = BeautifulSoup(response.body)
        to_store = 0
        print("Starting parse of one item! \n")
        bio = soup.find("table", {"class": "infobox biography vcard"})
        film_info = soup.find("table", {"class": "infobox vevent"})
        page_type = None
        if bio:
            bio = soup.find("table", {"class": "infobox biography vcard"})
            year, age = filter_actor_info(bio)
            if year != 0 and age != 0:
                item["actor_age"] = age
                item["actor_year"] = year
                page_type = "actor"
                item["page_type"] = page_type
                to_store = 1
        elif film_info:
            film_info = soup.find("table", {"class": "infobox vevent"})
            if film_info:
                film_info = soup.find("table", {"class": "infobox vevent"})
                logging.info("Filtering information for film")
                release_date = extract_release_date(film_info)
                film_dict = filter_film_info(film_info)
                if release_date is not None and film_dict is not None:
                    item["film_cast"] = film_dict['cast']
                    item["film_value"] = film_dict['box_office']
                    item["film_year"] = int(release_date)
                    page_type = "film"
                    item["page_type"] = page_type
                    to_store = 1

        if to_store:
            item['url'] = response.url
            name = soup.find("h1", {"id": "firstHeading"}).text
            item['name'] = name
            logging.debug("Returning from parsing of: " + response.url)
            if page_type == "film" and name not in films_seen:
                films_seen.append(name)
                films_parsed[name] = item
                return item
            elif page_type == "actor" and name not in actors_seen:
                actors_seen.append(name)
                actors_parsed[name] = item
                return item
            else:
                return None

        logging.warning("Page at: " + response.url + " is not a film or actor!")
        return None
