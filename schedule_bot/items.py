# -*- coding: utf-8 -*-
from scrapy_djangoitem import DjangoItem
from apps.core.models import Agenda
import scrapy


class ScheduleBotItem(DjangoItem):
    django_model = Agenda
    date = scrapy.Field()
    session = scrapy.Field()
    location = scrapy.Field()
    situation = scrapy.Field()
    comission = scrapy.Field()
