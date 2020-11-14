from django.shortcuts import render, HttpResponse, Http404
from migration import models


# Create your views here.
def get_home_page(request, name):
    try:
        user = models.User.objects.get(name=name)
        websiteSettings = models.WebsiteSettings.objects.get(websiteUser=user)
    except Exception as e:
        return HttpResponse("无用户")

    website_name = websiteSettings.websiteName
    json_info = {
        'websiteName': website_name,
    }

    posts = models.Post.objects.all()
    if posts is not None:
        json_info['posts'] = posts

    newest_posts = posts.order_by('-modifiedTime')
    if newest_posts is not None:
        json_info['newest_posts'] = newest_posts

    categories = models.Category.objects.all()
    if categories is not None:
        json_info['categories'] = categories
    tags = models.Tag.objects.all()
    if tags is not None:
        json_info['tags'] = tags
    print(json_info)
    return render(request, "homePage.html", context=json_info)
