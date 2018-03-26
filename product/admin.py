from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.admin import TranslationStackedInline
from zinnia.models import Entry
from zinnia.admin.entry import EntryAdmin
from product.models import *


class ZinniaEntryAdmin(TranslationAdmin, EntryAdmin):
    prepopulated_fields = {
        'slug_en': ('title_en',),
        'slug_el': ('title_el',),
        'slug_ru': ('title_ru',),
    }


class ImageInline(TranslationStackedInline):
    model = Image
    extra = 1


class ProjectAdmin(TranslationAdmin):
    list_display = ['slug', 'title', 'price', 'surface', 'status', 'promoted', 'slider', 'weight', 'date']
    list_filter = ['features', 'categories', 'status', 'promoted', 'slider']
    inlines = [ImageInline]

    fieldsets = [
        ('General', {'fields': ['slug', 'features', 'long', 'lat', 'price', 'surface', 'bedrooms',
                                'bathrooms', 'comment']}),
        ('Descriptions (el)', {'fields': ['title_el', 'general_description_el', 'location_description_el',
                                          'interior_description_el', 'exterior_description_el', 'call2action_el']}),
        ('Descriptions (en)', {'fields': ['title_en', 'general_description_en', 'location_description_en',
                                          'interior_description_en', 'exterior_description_en', 'call2action_en']}),
        ('Descriptions (ru)', {'fields': ['title_ru', 'general_description_ru', 'location_description_ru',
                                          'interior_description_ru', 'exterior_description_ru', 'call2action_ru']}),
        ('Publish', {'fields': ['status', 'promoted', 'promote_weight', 'slider', 'slider_weight', 'weight', 'date']}),
    ]


class FeatureAdmin(TranslationAdmin):
    pass


class ImageAdmin(TranslationAdmin):
    pass


admin.site.unregister(Entry)
admin.site.register(Entry, ZinniaEntryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Category)
