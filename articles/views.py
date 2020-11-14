from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from migration import models
# Create your views here.


def get_website_name(requests, json_info):
    user = models.User.objects.get(name=requests.session['user'])
    website_name = models.WebsiteSettings.objects.get(websiteUser=user).websiteName
    json_info['websiteName'] = website_name
    return json_info


def get_article_page(requests, post_id):
    post = models.Post.objects.get(id=int(post_id))
    post.views += 1
    json_info = {}

    json_info = get_website_name(requests, json_info)
    json_info['post'] = post
    json_info['from_user'] = requests.session['user']

    newest_posts = models.Post.objects.order_by("modifiedTime").all()
    newest_posts = newest_posts[5] if len(newest_posts) >= 5 else newest_posts
    json_info['newest_posts'] = newest_posts
    categories = models.Category.objects.all()
    json_info['categories'] = categories
    tags = models.Tag.objects.all()
    json_info['tags'] = tags

    body = post.body
    lines = body.replace("\r", "").split("\n")
    json_info['lines'] = lines
    post.save(update_fields=['views'])
    return render(requests, "articles.html", json_info)
