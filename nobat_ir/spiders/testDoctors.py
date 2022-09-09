# -*- coding: utf-8 -*-
import scrapy
import json

class GetdoctorsSpider(scrapy.Spider):
    name = 'testDoctor'
    allowed_domains = ['nobat.ir']
    start_urls = ['https://nobat.ir/doctor/%D8%AF%DA%A9%D8%AA%D8%B1-%D8%B9%D9%84%DB%8C-%D8%A7%D8%B5%D8%BA%D8%B1-%D8%AF%D8%B1%D8%AF%D8%B4%D8%AA%DB%8C-%D8%AA%D9%87%D8%B1%D8%A7%D9%86/dr-wqyk/']

    def parse(self, response):
        data = {
            'area': "blah blah",
            'field': "blah blah",
            'name': response.css("h1::text").get(),
            'field_in_detail': response.css(".nobat-blue-color::text").get(),
            'address': response.css("strong.text-justify.color-999::text").get(),
            'bioContent': response.css(".bioContent::text").get()
        }
        telID= response.css(".telShowStar").attrib['tel']
        offID= response.css(".telShowStar").attrib['off']
        formdata={'telID':telID,"offID":offID,"type":"dir"}
        yield scrapy.FormRequest("https://nobat.ir/office/page/inc_office_page/getTel1",formdata=formdata,callback=self.save_phone_detail,meta=data)

    def save_phone_detail(self, response):
        telephone = response.css("a::text").getall()
        data= {
                'area': response.meta.get('area'),
                'field': response.meta.get('field'),
                'name': response.meta.get('name'),
                'address': response.meta.get('address'),
                'field_in_detail': response.meta.get('field'),
                'bioContent':response.meta.get('bioContent'),
                'telephone':telephone,
            }
        yield data
        
            