from django.shortcuts import render, get_object_or_404
from .models import Post, Respuesta_usuario
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
    if request.method == 'POST':
        request.POST.get('name')
        respuestas = ''
        if Respuesta_usuario.objects.filter(usuario = request.user).exists():
            respuesta_usuario = Respuesta_usuario.objects.get(usuario = request.user)

        else:
            respuesta_usuario = Respuesta_usuario()
            respuesta_usuario.usuario = request.user
            respuesta_usuario.respuesta = str([0 for i in range(x)])[1:-1].replace(" ", "")

        lista = respuesta_usuario.respuesta.strip().split(',')

        for i, pregunta, tipo, cantidad in l:
            if tipo == '0':      
                if request.POST.get(str(i)) == '0':
                    n = int(lista[i])
                    n += 1
                    lista[i] = str(n)
                else:
                    n = int(lista[i])
                    n -= 1
                    lista[i] = str(n)
            elif tipo == '1':
                if request.POST.get(str(i)) > cantidad:
                    n = int(lista[i])
                    n -= 1
                    lista[i] = str(n) 
                else:
                    n = int(lista[i])
                    n += 1
                    lista[i] = str(n)
            elif tipo == '2':
                if request.POST.get(str(i)) == '0':
                    n = int(lista[i])
                    n += 1
                    lista[i] = str(n)
                else:
                    n = int(lista[i])
                    n -= 1
                    lista[i] = str(n)

        respuesta_usuario.respuesta = ','.join(lista)
        respuesta_usuario.save()
    return render(request, 'cuestionario.html', {'preguntas' : l})