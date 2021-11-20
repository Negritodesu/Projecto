from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.staticfiles import finders
# Create your views here.

def home(request):

    all_posts = Post.newmanager.all()



    return render(request, 'index.html', {'posts' : all_posts})

def post_single(request, post):

    post = get_object_or_404(Post, slug=post, status='published')

    return render(request, 'single.html', {'post' : post})

def cuestionario(request):
    result = finders.find('preguntas.csv')
    searched_locations = finders.searched_locations
    test = open(result)
    l =[]
    x = 0
    for linea in test:
        l2 = [x] + linea.strip().split(',')
        l.append(l2)
        x += 1

    
    return render(request, 'cuestionario.html', {'preguntas' : l})