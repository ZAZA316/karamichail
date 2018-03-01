from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


class Feature(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    icon = models.ImageField(verbose_name=_('Icon'), upload_to='features/')

    class Meta:
        verbose_name = _('Feature')
        verbose_name_plural = _('Features')


class Category(models.Model):
    description = RichTextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Project(models.Model):
    STATUS = (
        (0, _('archived')),
        (1, _('rented')),
        (2, _('sold')),
        (3, _('renting')),
        (4, _('in sale')),
        (5, _('future')),
    )

    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    general_description = RichTextField(verbose_name=_('General Description'))
    location_description = RichTextField(verbose_name=_('Location Description'), blank=True)
    interior_description = RichTextField(verbose_name=_('Interior Description'), blank=True)
    exterior_description = RichTextField(verbose_name=_('Exterior Description'), blank=True)
    features = models.ManyToManyField(Feature, related_name='product_feature', blank=True)
    long = models.FloatField(verbose_name=_('Longitude'))
    lat = models.FloatField(verbose_name=_('Latitude'))
    call2action = models.CharField(verbose_name=_('Call to Action'), max_length=255)
    categories = models.ManyToManyField(Category, related_name='product_category')
    price = models.DecimalField(verbose_name=_('Price'), max_digits=10, decimal_places=2, blank=True, null=True)
    surface = models.IntegerField(verbose_name=_('Surface'), blank=True, null=True)
    bedrooms = models.IntegerField(verbose_name=_('Bedrooms'), blank=True, null=True)
    bathrooms = models.IntegerField(verbose_name=_('Bathrooms'), blank=True, null=True)
    comment = RichTextField(verbose_name=_('Comment'), blank=True)
    status = models.IntegerField(verbose_name=_('Status'), choices=STATUS)
    promoted = models.BooleanField(verbose_name=_('Promoted'), default=False)
    promote_weight = models.IntegerField(verbose_name=_('Promote Weight'), default=0)
    slider = models.BooleanField(verbose_name=_('Slider'), default=False)
    slider_weight = models.IntegerField(verbose_name=_('Slider Weight'), default=0)
    date = models.DateField(verbose_name=_('Date'), auto_now_add=True)
    weight = models.IntegerField(verbose_name=_('Weight'), default=0)

    def __str__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        # return (en|el|ru)/projects/{slug}
        return '/projects/' + self.slug

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-date', 'weight', 'id']


class Image(models.Model):
    POSITION = (
        (0, _('wide')),
        (1, _('narrow')),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_('Image'), upload_to='projects/')
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    comment = models.CharField(verbose_name=_('Comment'), max_length=255, blank=True)
    position = models.IntegerField(verbose_name=_('Position'), choices=POSITION)
    weight = models.IntegerField(verbose_name=_('Weight'), default=0)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ['weight', 'id']
