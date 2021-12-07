from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Respuesta_usuario
from django.contrib.staticfiles import finders

# Create your views here.

def home(request):

    if not request.user.is_authenticated:
        return redirect('/account/login/')

    
    if Respuesta_usuario.objects.filter(usuario = request.user).exists():
        respuesta_usuario = Respuesta_usuario.objects.get(usuario = request.user)
        l_consejos = []
        l_valor = {}
        dicc_consejos = {}
        x = 0
        l = respuesta_usuario.respuesta.split(',')
        for respuestas in l:
            if int(respuestas) < 4 and int(respuestas) >-4:
                i = []
                i.append(respuestas)
                if int(respuestas) > 0:
                   i.append(0)
                else:
                    i.append(1)

                l_valor[x] = tuple(i)
            x+=1
        
        result = finders.find('consejos.csv')
        test = open(result,encoding="utf-8")
        x = 0
        for linea in test:
            l2 = [x] + [linea.strip().split('-')]
            l_consejos.append(l2)
            x += 1
        for linea in l_consejos:
            for valor in l_valor:
                if linea[0] == valor and l_valor[valor][1] == 0:
                    dicc_consejos[linea[0]] = linea[1][1]
                elif linea[0] == valor and l_valor[valor][1] == 1:
                    dicc_consejos[linea[0]] = linea[1][0]



        return render(request, 'index.html', {'consejos' : dicc_consejos})

    else:
        respuesta_usuario = Respuesta_usuario()
        respuesta_usuario.usuario = request.user
    

    return render(request, 'index.html')

def post_single(request, post):

    post = get_object_or_404(Post, slug=post, status='published')

    return render(request, 'single.html', {'post' : post})

def cuestionario(request):
    result = finders.find('preguntas.csv')
    test = open(result,encoding="utf-8")
    l =[]
    x = 0
    for linea in test:
        l2 = [x] + linea.strip().split('-')
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
            if tipo == '0' or tipo == 2:      
                if request.POST.get(str(i)) == '0':
                    n = int(lista[i])
                    n += 1
                    lista[i] = str(n)
                elif request.POST.get(str(i)) == '1':
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

        respuesta_usuario.respuesta = ','.join(lista)
        respuesta_usuario.save()
    return render(request, 'cuestionario.html', {'preguntas' : l})

def consejo(request, id_consejos):
    respuesta_usuario = Respuesta_usuario.objects.get(usuario = request.user)
    l_consejos = []
    l_valor = {}
    dicc_consejos = {}
    x = 0
    l = respuesta_usuario.respuesta.split(',')
    for respuestas in l:
        if int(respuestas) < 4 and int(respuestas) >-4:
            i = []
            i.append(respuestas)
            if int(respuestas) > 0:
                i.append(0)
            else:
                i.append(1)

            l_valor[x] = tuple(i)
        x+=1
        
    result = finders.find('consejos.csv')
    test = open(result,encoding="utf-8")
    x = 0
    for linea in test:
        l2 = [x] + [linea.strip().split('-')]
        l_consejos.append(l2)
        x += 1
    for linea in l_consejos:
        for valor in l_valor:
            if linea[0] == valor and l_valor[valor][1]== 0:
                dicc_consejos[linea[0]] = [linea[1][1],linea[1][2]]
            elif linea[0] == valor and l_valor[valor][1] == 1:
                dicc_consejos[linea[0]] = [linea[1][0],linea[1][2]]
    
    for consejos in dicc_consejos:
        if id_consejos == consejos:
            consejo = []
            consejo.append(id_consejos)
            consejo.append(dicc_consejos[consejos])
            


    return render(request, 'consejos.html', {'consejo' : consejo})