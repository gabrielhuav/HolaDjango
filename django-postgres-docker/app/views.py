from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Usuario
from .forms import UsuarioForm, LoginForm

def index(request):
    user_info = ""
    if 'usuario_id' in request.session:
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            user_info = f"<p>Bienvenido, {usuario.nombre}! <a href='/logout/'>Cerrar sesión</a></p>"
        except Usuario.DoesNotExist:
            pass
    else:
        user_info = "<p><a href='/login/'>Iniciar sesión</a> | <a href='/registro/'>Registrarse</a></p>"
    
    return HttpResponse(f"<h1>¡Hola, Django desde Docker!</h1>{user_info}<br><a href='/usuarios/'>Ver usuarios</a>")

def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario registrado exitosamente!')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    
    return render(request, 'registro.html', {'form': form})

def lista_usuarios(request):
    # Verificar si el usuario está logueado
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para ver la lista de usuarios.')
        return redirect('login_usuario')
    
    # Verificar que el usuario existe en la base de datos
    try:
        Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.')
        return redirect('login_usuario')
    
    usuarios = Usuario.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_rol'] = usuario.rol
            messages.success(request, f'¡Bienvenido, {usuario.nombre}!')
            return redirect('index')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_usuario(request):
    request.session.flush()
    messages.success(request, '¡Sesión cerrada exitosamente!')
    return redirect('index')