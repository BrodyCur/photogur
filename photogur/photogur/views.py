from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.shortcuts import render, reverse, redirect
from photogur.models import Picture, Comment
from django.views.decorators.http import require_http_methods
from photogur.forms import LoginForm
from django.contrib.auth import authenticate, login

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

@require_http_methods(['POST'])
def create_comment(request):
  picture_id = request.POST['picture']
  picture = Picture.objects.get(id=picture_id)
  comment_name = request.POST['comment-name']
  comment_msg = request.POST['comment-body']
  Comment.objects.create(name=comment_name, message=comment_msg, picture=picture)
  return redirect('picture_details', id=picture.id)

def login_view(request):
  if request.method == 'POST':
    form =LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      pw = form.cleaned_data['password']
      user = authenticate(username=username, password=pw)
      if user is not None:
        login(request, user)
        return redirect('home')
      else:
        form.add_error('username', 'Login failed')
  else:
    form = LoginForm()

  context = {
    'form': form
  }
  response = render(request, 'login.html', context)
  return HttpResponse(response)

