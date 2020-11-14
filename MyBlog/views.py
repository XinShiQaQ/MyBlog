from django.shortcuts import HttpResponseRedirect, HttpResponse


def get_home_page(requests):
    return HttpResponseRedirect('/user/xinshi')
