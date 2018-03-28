from django.shortcuts import render, redirect
from django.utils import translation

from product.models import *


def home_page(request):
    projects = Project.objects.filter(status__gt=0).filter(slider=True).order_by('slider_weight')[:6]
    slides = []
    for project in projects:
        slide = {'title': project.title}
        image = project.image_set.all().filter(position=0).order_by('weight')[0]
        slide['image'] = image.image
        slides.append(slide)

    fprojects = Project.objects.filter(status__gt=0).filter(promoted=True).order_by('promote_weight')[:6]
    fimages = []
    for project in fprojects:
        image = project.image_set.all().filter(position=1).order_by('weight')[0]
        fimages.append(image.image)

    context = {'slides': slides, 'projects': fprojects, 'images': fimages}
    return render(request, 'product/index.html', context=context)


def company_page(request):
    return render(request, 'product/about.html')


def projects_page(request):
    projects = Project.objects.filter(status__gt=0).order_by('weight')
    locations = []
    for project in projects:
        locations.append([project.title, project.long, project.lat])

    images = []
    for project in projects:
        image = project.image_set.all().filter(position=0).order_by('weight')[0]
        images.append(image.image)

    context = {'projects': projects, 'images': images, 'locations': locations}
    return render(request, 'product/projects.html', context=context)


def project_page(request, slug):
    project = Project.objects.get(slug=slug)
    images = []
    features = []
    for image in project.image_set.all():
        images.append(image.image)
    for feature in project.features.all():
        features.append(feature.name)
    features = [[features[i], features[i + 1]] if i < len(features) - 1 else [features[i], '&nbsp;']
                for i in range(0, len(features), 2)]

    fprojects = Project.objects.filter(status__gt=0).filter(promoted=True).order_by('promote_weight')[:6]
    fimages = []
    for fproject in fprojects:
        image = fproject.image_set.all().filter(position=1).order_by('weight')[0]
        fimages.append(image.image)

    context = {'project': project, 'images': images, 'features': features, 'fprojects': fprojects, 'fimages': fimages}
    return render(request, 'product/project-info.html', context=context)


def contact_page(request):
    return render(request, 'product/contact.html')


def blog_page(request):
    return render(request, 'product/blog1.html')


def switch_language(request, language):
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language
    return redirect('/admin')
