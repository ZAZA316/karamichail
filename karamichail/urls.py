"""karamichail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from product.views import *


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

    url(r'^admin/', admin.site.urls),

    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django_comments.urls')),

    url(r'^rosetta/', include('rosetta.urls')),

    path('i18n/', include('django.conf.urls.i18n')),
    path('language/<language>/', switch_language),

    url(r'^$', home_page, name='home_page'),
    url(r'^about/', company_page, name='company_page'),
    url(r'^projects/', projects_page, name='projects_page'),
    url(r'^project/(?P<slug>[\w-]+)/$', project_page, name='project_page'),
    url(r'^contact/', contact_page, name='contact_page'),
    url(r'^blog/', blog_page, name='blog_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns