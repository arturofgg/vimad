from django.urls import path
from . import views

app_name = 'vimad'
urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/', views.perfil, name='perfil'),
    path('video/<slug:slug>/', views.video, name='video'),
    path('ficha/<slug:slug>/', views.ficha, name='ficha'),
    path('login/', views.inicio, name='inicio'),
    path('register/', views.register, name='register'),
    path('logout/', views.signout, name='logout'),
    path('about/',views.about, name='about'),
    path('generos/', views.generos, name='generos'),
    path('generos/<str:genero>/', views.cortos_por_genero, name='cortos_por_genero'),
    path('buscar/', views.buscar, name='buscar'),
]