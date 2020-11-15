from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from migration import models


# Create your views here.
def get_home_page(request, visiting_author_name=""):
    print(visiting_author_name)
    if visiting_author_name == "":
        return HttpResponseRedirect('/xinshi')
    try:
        visiting_author = models.User.objects.get(name=visiting_author_name)
        website_settings = models.WebsiteSettings.objects.get(websiteUser=visiting_author)
    except Exception as e:
        return HttpResponse("无用户")

    website_name = website_settings.websiteName
    json_info = {
        'websiteName': website_name,
        'website_owner_name': website_settings.websiteUser.name
    }
    request.session['website_owner_name'] = website_settings.websiteUser.name
    posts = models.Post.objects.all().order_by('-modifiedTime')
    if posts is not None:
        json_info['posts'] = posts

    newest_posts = posts.order_by('-modifiedTime')
    newest_posts = newest_posts[5] if len(newest_posts) >= 5 else newest_posts
    if newest_posts is not None:
        json_info['newest_posts'] = newest_posts

    categories = models.Category.objects.filter(owner__name__contains=request.session['website_owner_name'])
    print(type(categories))
    print(categories)
    if categories is not None:
        json_info['categories'] = categories
    tags = models.Tag.objects.filter(owner__name__contains=request.session['website_owner_name'])
    if tags is not None:
        json_info['tags'] = tags
    print(json_info)
    return render(request, "homePage.html", context=json_info)
