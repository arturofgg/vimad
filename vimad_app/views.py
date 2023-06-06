from django.shortcuts import render,  get_object_or_404, redirect
from django.http import JsonResponse
from .models import Corto
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, CustomAuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re


# index - LISTADO DE CORTOS INICIAL - LISTADO DE CORTOS POR GENERO, IDIOMA, etc

def index(request, genero=None, idioma=None):
    cortos = Corto.objects.all().order_by('-id')[:10]
    cortos_animacion = list(Corto.objects.filter(
        genero='animacion').order_by('?'))[:10]
    cortos_espanol = list(Corto.objects.filter(
        idioma='español').order_by('?'))[:10]
    return render(request, 'vimad_app/index.html', {'cortos': cortos, 'cortos_animacion': cortos_animacion, 'cortos_espanol': cortos_espanol})

# LISTADO DE GENEROS


def generos(request):
    generos = Corto.objects.values_list('genero', flat=True).distinct()
    return render(request, 'vimad_app/generos.html', {'generos': generos})

# VISTA DE CORTOS POR GENERO


def cortos_por_genero(request, genero):
    cortos = Corto.objects.filter(genero=genero)
    titulo = "Cortos de " + genero
    return render(request, 'vimad_app/cortos_por_genero.html', {'cortos': cortos, 'titulo': titulo})

# about


def about(request):
    return render(request, 'vimad_app/about.html')

# perfil


@login_required(login_url='vimad:inicio')
def perfil(request):
    return render(request, 'vimad_app/perfil.html')

# sesion


@login_required(login_url='vimad:inicio')
def sesion(request):
    return render(request, 'vimad_app/sesion.html')

# video


@login_required(login_url='vimad:inicio')
def video(request, slug):
    corto = get_object_or_404(Corto, slug=slug)
    if not corto.video:
        return redirect('vimad:index')
    return render(request, 'vimad_app/video.html', {'video_url': corto.video.url})

# ficha - USO DE MODELOS COGIENDO slug POR URL


def ficha(request, slug):
    corto = get_object_or_404(Corto, slug=slug)
    directores = corto.director.all()
    actores = corto.actor.all()
    estudio = corto.estudio

    context = {
        'corto': corto,
        'directores': directores,
        'actores': actores,
        'estudio': estudio
    }

    return render(request, 'vimad_app/ficha.html', context)


# BUSCADOR


def buscar(request):
    query = request.GET.get('q', '')
    cortos = Corto.objects.filter(
        Q(titulo__icontains=query) |
        Q(genero__icontains=query) |
        Q(idioma__icontains=query) |
        Q(pais__icontains=query)
    )

    cortos_list = []
    for corto in cortos:
        cortos_list.append({
            'id': corto.id,
            'titulo': corto.titulo,
            'genero': corto.genero,
            'idioma': corto.idioma,
            'pais': corto.pais,
            'imagen': corto.imagen.url,
            'slug': corto.slug,
        })

    return JsonResponse({'cortos': cortos_list})

# register


def register(request):
    if request.user.is_authenticated:
        return redirect('vimad:index')
    else:
        if request.method == 'GET':
            return render(request, 'vimad_app/register.html', {
                'form': CreateUserForm
            })
        else:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            try:
                # Validar el nombre de usuario
                validate_username(username)
            except ValidationError as e:
                return render(request, 'vimad_app/register.html', {
                    'form': CreateUserForm,
                    "error": ' '.join(e.messages),
                })

            try:
                # Validar el formato del correo electrónico
                validate_email(email)
            except ValidationError:
                return render(request, 'vimad_app/register.html', {
                    'form': CreateUserForm,
                    "error": 'Por favor, introduce un correo electrónico válido',
                })
            
            try:
                # Validar la contraseña
                validate_password(password1, username)
            except ValidationError as e:
                return render(request, 'vimad_app/register.html', {
                    'form': CreateUserForm,
                    "error": ' '.join(e.messages),
                })

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    return render(request, 'vimad_app/register.html', {
                        'form': CreateUserForm,
                        "error": 'Este correo electrónico ya está registrado',
                    })
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password1
                    )
                    user.save()
                    login(request, user)
                    return redirect('vimad:index')
                except IntegrityError:
                    return render(request, 'vimad_app/register.html', {
                        'form': CreateUserForm,
                        "error": 'Ya hay un usuario con este nombre',
                    })
            else:
                return render(request, 'vimad_app/register.html', {
                    'form': CreateUserForm,
                    "error": 'Las contraseñas no coinciden',
                })

# validacion del nombre de usuario


def validate_username(username):
    if len(username) < 3 or len(username) > 16:
        raise ValidationError('El nombre de usuario debe tener entre 3 y 16 caracteres.')

    if not re.match(r'^[\w.@+-]+$', username):
        raise ValidationError('El nombre de usuario solo puede contener letras, dígitos y los caracteres @/./+/-/_.')
    
# validacion contraseña


def validate_password(password, username=None):
    if len(password) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres.')

    if len(password) > 20:
        raise ValidationError('La contraseña no puede tener más de 20 caracteres.')

    if username and username.lower() in password.lower():
        raise ValidationError('La contraseña no puede contener el nombre de usuario.')

    # if not re.search(r'\d', password):
    #     raise ValidationError('La contraseña debe contener al menos un número.')
    
    # if not re.search(r'[A-Z]', password):
    #     raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
    
    # if not re.search(r'[a-z]', password):
    #     raise ValidationError('La contraseña debe contener al menos una letra minúscula.')

    # if not re.search(r'[\W_]', password):
    #     raise ValidationError('La contraseña debe contener al menos un carácter especial.')

# login


def inicio(request):
    if request.user.is_authenticated:
        return redirect('vimad:index')
    else:
        if request.method == 'GET':
            return render(request, 'vimad_app/inicio.html', {
                'form': CustomAuthenticationForm
            })
        else:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'vimad_app/inicio.html', {
                    'form': CustomAuthenticationForm,
                    'error': 'Usuario o contraseña incorrectos'
                })
            else:
                login(request, user)
                return redirect('vimad:index')

# logout


def signout(request):
    logout(request)
    return redirect('vimad:inicio')