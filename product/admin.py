from django.contrib import admin

from product.models import *


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'price', 'surface', 'status', 'promoted', 'slider', 'weight', 'date']
    list_filter = ['features', 'categories', 'status', 'promoted', 'slider']
    inlines = [ImageInline]

    fieldsets = [
        ('General', {'fields': ['slug', 'title', 'features', 'categories']}),
        ('Descriptions', {'fields': ['general_description', 'location_description',
                                     'interior_description', 'exterior_description',
                                     'comment', 'call2action']}),
        ('Details', {'fields': ['long', 'lat', 'price', 'surface', 'bedrooms', 'bathrooms']}),
        ('Publish', {'fields': ['status', 'promoted', 'promote_weight', 'slider', 'slider_weight', 'weight', 'date']}),
    ]


class FeatureAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
