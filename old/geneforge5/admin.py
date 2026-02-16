# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import ItemVariety, Stat, ObjectTemplate, ItemTemplate, ItemStat, Zone, ZoneObject, ZoneItem, CreatureTemplate,  ZoneCreature, CreatureTemplateItemDrop

admin.site.register(ItemVariety)
admin.site.register(Stat)
admin.site.register(ObjectTemplate)
admin.site.register(ItemTemplate)
admin.site.register(ItemStat)
admin.site.register(Zone)
admin.site.register(ZoneObject)
admin.site.register(ZoneItem)
admin.site.register(CreatureTemplate)
admin.site.register(ZoneCreature)
admin.site.register(CreatureTemplateItemDrop)
