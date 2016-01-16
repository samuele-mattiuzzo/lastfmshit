import scrapy
import datetime
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from lastfm.items import LastfmItem

collected_artists = []

def similar_artist(artists, urls):
    both = zip(artists, urls)
    similar = []

    for artist in both:
        if artist[0] in collected_artists:
            pass
        else:
            if "'" not in artist[0]:
                similar.append(artist)
            else:
                pass

    try:
        return similar[0]
    except:
        return ''

all_items = []
class LastfmSpider(scrapy.Spider):
    name = "lastfmspider"
    allowed_domains = ["last.fm"]
    start_urls = [
        "http://www.last.fm/music/Alien+Ant+Farm"
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse", follow= True),
    )

    def parse(self, response):
        artist = response.xpath('//*[@id="content"]/header/div[2]/div/div[2]/div[1]/div[1]/h1/text()').extract()
        img_url = response.xpath('//*[@id="content"]/header/div[2]/div/div[1]/div/a/img/@src').extract()
        artist_listens = response.xpath('//*[@id="content"]/header/div[2]/div/div[2]/div[2]/div/table/tbody/tr/td[2]/abbr/@title').extract()
        genre = response.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section[1]/ul/li[1]/a/text()').extract()
        top_track = response.xpath('//*[@id="top-tracks-section"]/div/table/tbody/tr[1]/td[4]/span/a/text()').extract()
        top_track_listens = response.xpath('//*[@id="top-tracks-section"]/div/table/tbody/tr[1]/td[5]/span/span/span/text()').extract()
        related_artists_names = response.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section[5]/ol/li[contains(@class, "grid-items-item")]/div/div/p[1]/a/text()').extract()
        related_artists_urls = response.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section[5]/ol/li[contains(@class, "grid-items-item")]/div/div/p[1]/a/@href').extract()

        item = LastfmItem()
        artist_whitespace = re.sub('\s+',' ',artist[0])
        item['artist'] = artist_whitespace.strip()
        collected_artists.append(item['artist'])
        item['arist_url'] = response.url
        item['img_url'] = img_url[0]
        item['artist_listens'] = re.sub('[^0-9]','', artist_listens[0])
        item['genre'] = genre[0]
        item['top_track'] = top_track[0]
        lol = re.sub('\s+',' ',top_track_listens[0])
        top_track_listens_whitespace = re.sub('[^0-9]','', lol)
        item['top_track_listens'] = top_track_listens_whitespace.strip()
        related_artist = similar_artist(related_artists_names, related_artists_urls)

        
        try:
            item['similar_artist'] = related_artist[0]
            item['similar_artist_url'] = related_artist[1]
        except IndexError:
            item['similar_artist'] = ''
            item['similar_artist_url'] = ''
            request = scrapy.Request(response.url+'/+similar',
                     callback=self.parse_related)
            request.meta['item'] = item
            yield request
            return
        else:
            url = 'http://last.fm{}'.format(''.join(item['similar_artist_url']))
            url = scrapy.utils.url.escape_ajax(scrapy.utils.url.safe_url_string(url))
            print "Artists:", collected_artists
            all_items.append(item)
            
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse)
        yield item
            

        
    def parse_related(self, response):
        related_artists_names = response.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section/ol/li/div[1]/div/div/p[1]/a/text()').extract()
        related_artists_urls = response.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section/ol/li/div[1]/div/div/p[1]/a/@href').extract()
        
        related_artist = similar_artist(related_artists_names, related_artists_urls)

        item = response.meta['item']
        
        item['similar_artist'] = related_artist[0]
        item['similar_artist_url'] = related_artist[1]

        url = 'http://last.fm{}'.format(''.join(item['similar_artist_url']))
        print "Artists:", collected_artists
        all_items.append(item)
        
        yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse)
        return
        

print all_items




