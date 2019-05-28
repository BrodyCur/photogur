from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.shortcuts import render, reverse, redirect
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

def picture_search(request):
  query = request.GET['query']
  search_results = Picture.objects.filter(artist=query)
  context = {
    'pictures': search_results,
    'query': query,
  }
  response = render(request, 'search.html', context)
  return HttpResponse(response)


def create_comment(request):
  picture_id = request.POST['picture']
  picture = Picture.objects.get(id=picture_id)
  comment_name = request.POST['comment-name']
  comment_msg = request.POST['comment-body']
  Comment.objects.create(name=comment_name, message=comment_msg, picture=picture)
  return redirect('picture_details', id=picture.id)