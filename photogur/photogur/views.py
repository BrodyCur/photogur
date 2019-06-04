from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.shortcuts import render, reverse, redirect, get_object_or_404
from photogur.models import Picture, Comment
from django.views.decorators.http import require_http_methods
from photogur.forms import LoginForm, PictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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

def logout_view(request):
  logout(request)
  return redirect('home')

def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=raw_password)
      login(request, user)
      return redirect('home')
  else:
    form = UserCreationForm()

  response = render(request, 'signup.html', {'form': form})
  return HttpResponse(response)

@login_required
def new_picture(request):
  if request.method == 'POST':
    form = PictureForm(request.POST)
    if form.is_valid():
      picture = form.save(commit=False)
      picture.user = request.user
      picture.save()
      return redirect('picture_details', id=picture.id)
  else:
    form = PictureForm()
  context = {
    'form': form
  }
  return render(request, 'createpic.html', context)

@login_required
def edit_picture(request, id):
  picture = get_object_or_404(Picture, pk=id, user=request.user.pk)
  form = PictureForm(instance=picture)
  context = {
    'form': form
  }
  return render(request, 'editpic.html', context)