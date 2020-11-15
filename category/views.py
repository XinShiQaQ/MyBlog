from django.shortcuts import render, HttpResponse
from migration import models
# Create your views here.
def get_category_page(requests, cate_id):
    visiting_author_name = requests.session['website_owner_name']
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

    posts = models.Post.objects.filter(author=visiting_author, category_id=int(cate_id)).order_by('modifiedTime')
    json_info['posts'] = posts

    newest_posts = posts.order_by('modifiedTime')
    newest_posts = newest_posts[5] if len(newest_posts) >= 5 else newest_posts
    json_info['newest_posts'] = newest_posts

    categories = models.Category.objects.filter(owner__name__contains=visiting_author_name)
    json_info['categories'] = categories
    tags = models.Tag.objects.filter(owner__name__contains=visiting_author_name)
    json_info['tags'] = tags
    return render(requests, "category.html", context=json_info)