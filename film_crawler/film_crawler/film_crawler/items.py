# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FilmCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    page_type = scrapy.Field()

    film_cast = scrapy.Field()
    film_year = scrapy.Field()
    film_value = scrapy.Field()

    # Year (weather born or film production)
    actor_year = scrapy.Field()
    actor_age = scrapy.Field()