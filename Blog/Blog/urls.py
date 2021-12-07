from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name = 'homepage'),
    path('cuestionario/', views.cuestionario, name = 'cuestionario'),
    path('<slug:post>/', views.post_single, name='post_single'),
    path('consejos/<int:id_consejos>/', views.consejo, name = 'consejos')
]