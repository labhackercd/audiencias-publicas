# -*- coding: utf-8 -*-
import scrapy
from schedule_bot.items import ScheduleBotItem
from scrapy.selector import Selector
from datetime import datetime
from apps.core.models import Agenda


class AgendaSpider(scrapy.Spider):
    name = "agenda"
    allowed_domains = ["http://www.camara.leg.br/"]
    start_urls = (
        'http://www.camara.leg.br/internet/ordemdodia/ordemComGeral.asp',
    )

    def parse(self, response):
        Agenda.objects.all().delete()
        for sessionbox in Selector(response=response).xpath('//div[@class="sessionBox"]'):
            for line in sessionbox.xpath('table/tbody[1]/tr'):
                commission = sessionbox.xpath('h4/text()').re('[^\t\n\r]+')[0]
                session = line.xpath('td[2]/strong/text()').re('[^\t\n\r]+')[1]
                location = line.xpath('td[2]/text()').re('[^\t\n\r]+')[0]
                situation = line.xpath('td[3]/text()|td[3]/strong/text()').re('[^\t\n\r]+')[0]
                str_date = line.xpath('td[1]/text()').re('[^\t\n\r]+')[0]
                dt = datetime.strptime(str_date, '%d/%m/%Y')
                hour = line.xpath('td[1]/text()').re('[^\t\n\r]+')[1].strip(' ').split('h')[0]
                minute = line.xpath('td[1]/text()').re('[^\t\n\r]+')[1].strip(' ').split('h')[1]
                if hour.isdigit():
                    hour = int(hour)
                else:
                    hour = 0
                if minute.isdigit():
                    minute = int(minute)
                else:
                    minute = 0
                date = dt.replace(hour=hour, minute=minute)
                item = ScheduleBotItem()
                if date:
                    item['date'] = date
                if commission:
                    item['commission'] = commission
                if session:
                    item['session'] = session
                if location:
                    item['location'] = location
                if situation:
                    item['situation'] = situation
                yield item
