# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LastfmItem(scrapy.Item):
    artist = scrapy.Field()
    arist_url = scrapy.Field()
    img_url = scrapy.Field()
    artist_listens = scrapy.Field()
    genre = scrapy.Field()
    top_track = scrapy.Field()
    top_track_listens = scrapy.Field()
    similar_artist = scrapy.Field()
    similar_artist_url = scrapy.Field()
    pass
