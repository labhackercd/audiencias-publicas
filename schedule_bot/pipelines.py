# -*- coding: utf-8 -*-
class ScheduleBotPipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item
