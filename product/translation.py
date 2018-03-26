from modeltranslation.translator import translator, TranslationOptions
from zinnia.models import Entry
from product.models import Project, Feature, Image


class ZinniaEntryTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'slug', 'excerpt')


class ProjectTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'general_description',
        'location_description',
        'interior_description',
        'exterior_description',
        'call2action',
    )


class FeatureTranslationOptions(TranslationOptions):
    fields = ('name',)


class ImageTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Entry, ZinniaEntryTranslationOptions)
translator.register(Project, ProjectTranslationOptions)
translator.register(Feature, FeatureTranslationOptions)
translator.register(Image, ImageTranslationOptions)
