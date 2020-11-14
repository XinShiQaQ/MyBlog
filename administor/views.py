from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from migration import models
from django.core.exceptions import ObjectDoesNotExist
import datetime
# Create your views here.


class NoInputError(Exception):
    pass


def get_website_name(requests, json_info):
    user = models.User.objects.get(name=requests.session['user'])
    website_name = models.WebsiteSettings.objects.get(websiteUser=user).websiteName
    json_info['websiteName'] = website_name
    return json_info


def get_modify_article_page(requests, post_id):
    json_info = {}
    get_website_name(requests, json_info)
    if 'user' not in requests.session:
        return HttpResponseRedirect("/admin")
    try:
        categories = models.Category.objects.all()
    except Exception:
        print("No category found will lead to exception")
        categories = None
    json_info['categories'] = categories
    if post_id != "new":
        post = models.Post.objects.get(id=int(post_id))
        json_info['post'] = post
    return render(requests, "admin/modifyArticles.html", json_info)


def get_admin_login_page(requests):
    json_info = {}
    if 'user' not in requests.session:
        user = models.User.objects.get(name="xinshi")
        website_name = models.WebsiteSettings.objects.get(websiteUser=user).websiteName
        json_info['websiteName'] = website_name
        return render(requests, "admin/adminLogin.html", json_info)
    else:
        return HttpResponseRedirect("/admin")


def check_login(requests):
    account = requests.POST.get('account')
    password = requests.POST.get('password')
    print(account, password)
    try:
        if not account or not password:
            raise NoInputError("未输入账户或密码")
        user = models.User.objects.get(account=account, password=password)
        if user:
            requests.session['user'] = user.name
            requests.session.set_expiry(60 * 60 * 8)
            return HttpResponseRedirect("/admin")
    except NoInputError as e:
        return HttpResponse(e)
    except ObjectDoesNotExist as e:
        return HttpResponse("用户名错误")


def get_admin_page(requests):
    if 'user' not in requests.session:
        return HttpResponseRedirect("/admin/Login")
    json_info = {}
    get_website_name(requests, json_info)
    user = models.User.objects.get(name=requests.session['user'])
    posts = models.Post.objects.filter(author=user).order_by("modifiedTime")
    json_info['posts'] = posts
    return render(requests, "admin/admin.html", json_info)


def quits(requests):
    requests.session.flush()
    return HttpResponseRedirect("/admin")


def modify_confirm(requests, post_id):
    title = requests.GET.get('title')
    body = requests.GET.get('body')
    excerpt = requests.GET.get('excerpt')
    if excerpt == "":
        excerpt = body[:100] if len(body) >= 100 else body
    category = requests.GET.get('category')
    tags = requests.GET.get('tags')
    modifyTime = datetime.datetime.now()
    author = models.User.objects.get(name=requests.session['user'])
    try:
        if category != "":
            category = models.Category.objects.get(categoryName=category)
    except Exception:
        category = models.Category.objects.create(categoryName=category)
    if tags != "":
        tags = tags.split(';')
        for i in range(len(tags)):
            try:
                tags[i] = models.Tag.objects.get(tagName=tags[i].strip())
            except Exception:
                tags[i] = models.Tag.objects.create(tagName=tags[i].strip())
    if post_id == "new":
        createTime = modifyTime
        post = models.Post(title=title, body=body, excerpt=excerpt, modifiedTime=modifyTime,
                           createTime=createTime, author=author)
        post.category = category
        post.save()
        for tag in tags:
            post.tag.add(tag)
        post.save()
    else:
        post = models.Post.objects.get(id=int(post_id))
        post.title = title
        post.body = body
        post.excerpt = excerpt
        post.modifiedTime = modifyTime
        post.category = category
        if post.tag:
            post.tag.all().delete()
        for tag in tags:
            post.tag.add(tag)
        post.save()
    return HttpResponseRedirect('/admin')

def delete_article(requests, post_id):
    try:
        post = models.Post.objects.get(id=post_id)
        post.delete()
        return HttpResponseRedirect('/admin')
    except Exception:
        return HttpResponse('删除失败')

