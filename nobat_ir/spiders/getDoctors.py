# -*- coding: utf-8 -*-
import scrapy
import json

class GetdoctorsSpider(scrapy.Spider):
    name = 'getDoctors'
    allowed_domains = ['nobat.ir']
    start_urls = ['https://nobat.ir/inc/nselectPlace']

    def parse(self, response):
        area_data=json.loads(response.text)
        for area in area_data:
            yield scrapy.Request(area['url'],callback=self.get_field,meta={'area': area['tit']})

    def get_field(self, response):
        fields = response.css("#specialtyFr>a")
        for field in fields:
            yield scrapy.Request(field.attrib['href'],callback=self.get_doctors,meta={'area': response.meta.get('area'),"field":field.css("::text")[1].get()})

    def get_doctors(self, response):
        doctors = response.css("a.drList")
        for doctor in doctors:
            yield scrapy.Request("https://nobat.ir"+doctor.attrib['href'],callback=self.get_detail,meta={'area': response.meta.get('area'),"field":response.meta.get('field')})

    def get_detail(self, response):
        data= {
                'area': response.meta.get('area'),
                'field': response.meta.get('field'),
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
        
            