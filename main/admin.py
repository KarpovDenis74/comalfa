from django.contrib import admin
from .models import *
# Register your models here..

admin.site.register(News)
admin.site.register(Documents)
# admin.site.register(EngineUnits)
# admin.site.register(Parts)
# admin.site.register(Gallery)
# admin.site.register(MainGoods)
admin.site.register(PopularUrl)


class GuidesAdmin(admin.TabularInline):
    model = SeriesEngineGuides
class EngineAdmin(admin.TabularInline):
    model = Engine

class Test(admin.TabularInline):
    model = EngineUnits

@admin.register(MainGoods)
class MainGoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'mark', 'type', 'price')
    search_fields = ['mark']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'img')

@admin.register(Engine)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'seriesEngine')

    inlines = [
        Test,
    ]

@admin.register(SeriesEngine)
class SeriesEngineAdmin(admin.ModelAdmin):
    inlines = [
        GuidesAdmin,
        EngineAdmin,
    ]

