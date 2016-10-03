# -*- coding: utf-8 -*-
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'audiencias_publicas.settings'
django.setup()

BOT_NAME = 'schedule_bot'

SPIDER_MODULES = ['schedule_bot.spiders']
NEWSPIDER_MODULE = 'schedule_bot.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'schedule_bot.pipelines.ScheduleBotPipeline': 1000,
}
