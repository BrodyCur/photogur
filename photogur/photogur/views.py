from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from photogur.models import Picture, Comment

def root(request):
  return HttpResponseRedirect('/pictures')

def pictures_page(request):
  context = {
'pictures': Picture.objects.all(),
'title': 'Gallery'
  }
  response = render(request, 'pictures.html', context)
  return HttpResponse(response)

def picture_show(request, id):
  picture = Picture.objects.get(pk=id)
  context = {
    'picture': picture,
    'title': picture.title
  }
  response = render(request, 'picture.html', context)
  return HttpResponse(response)