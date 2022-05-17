from gc import callbacks
import scrapy

#FILTER_LINK = //div[@id = "aspect_discovery_SimpleSearch_div_search-results"]/div[@class = "row ds-artifact-item "]//div[@class = "thumbnail artifact-preview"]/a/@href
#NEXT_BUTTON_LINK = //ul[@class = 'pagination']/a[@class = 'next-page-link']/@href

class first_spider(scrapy.Spider):
  name = 'unalr'
  start_urls = [
    'https://repositorio.unal.edu.co/discover?filtertype=subject&filter_relational_operator=equals&filter=62+Ingenier%C3%ADa+y+operaciones+afines+%2F+Engineering'
  ]
  custom_settings = {
    'FEED_URI' : 'links.json',
    'FEED_FORMAT' : 'json',
    'FEED_EXPORT_ENCODING': 'utf-8',
    'ROBOTSTXT_OBEY': False
  }

  def parse(self, response, **kwargs):
    if kwargs:
      links = kwargs['links']
    else:
      links = []

    links.extend(response.xpath('//div[@id = "aspect_discovery_SimpleSearch_div_search-results"]/div[@class = "row ds-artifact-item "]//div[@class = "thumbnail artifact-preview"]/a/@href').getall())   

    next_page_button_link = response.xpath(
      '//ul[@class = "pagination"]//li/a[@class = "next-page-link"]/@href'
    ).get()

    if next_page_button_link:
      yield response.follow(next_page_button_link, callback = self.parse, cb_kwargs = {'links': links})
    else:
      yield {
        'links' : links
      }



