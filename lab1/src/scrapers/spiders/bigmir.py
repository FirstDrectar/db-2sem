# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class BigmirSpider(scrapy.Spider):
    name = 'bigmir'
    allowed_domains = ['bigmir.net']
    start_urls = ['http://news.bigmir.net/']

    def parse(self, response: Response):
        all_images = response.xpath("//img/@src[starts-with(., 'http')]")
        all_text = response.xpath(
            "//*[not(self::script)][not(self::style)][string-length(normalize-space(text())) > 30]/text()")
        yield {
            'url': response.url,
            'payload': [{'type': 'text', 'data': text.get().strip()} for text in all_text] +
                       [{'type': 'image', 'data': image.get()} for image in all_images]
        }
        if response.url == self.start_urls[0]:
            all_ukr_links = response.xpath("//a/@href[starts-with(., '/ukraine/')]")
            all_world_links = response.xpath("//a/@href[starts-with(., '/world/')]")
            ukr_selected_links = [link.get() for link in all_ukr_links][:19]
            world_selected_links = [link.get() for link in all_world_links][:19]
            selected_links=ukr_selected_links+world_selected_links
            print(selected_links)
            for link in selected_links:
                yield scrapy.Request("http://news.bigmir.net/"+link, self.parse)
