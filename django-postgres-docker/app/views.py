from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Usuario, Favorito
from .forms import UsuarioForm, LoginForm, AnimeSearchForm
import requests

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

def buscar_anime(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para buscar anime.')
        return redirect('login_usuario')

    try:
        current_user = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión no es válida. Por favor, inicia sesión nuevamente.')
        return redirect('login_usuario')

    form = AnimeSearchForm()
    resultados_api = None # Renombrado para claridad
    error_api = None
    
    # Obtener IDs de animes favoritos del usuario actual
    favoritos_ids = list(Favorito.objects.filter(usuario=current_user).values_list('anime_id', flat=True))

    if request.method == 'GET' and 'query' in request.GET:
        form = AnimeSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            try:
                response = requests.get(f'https://api.jikan.moe/v4/anime?q={query}&sfw')
                response.raise_for_status()
                resultados_api = response.json().get('data', [])
            except requests.exceptions.RequestException as e:
                error_api = f"Error al conectar con la API de Jikan: {e}"
            except ValueError:
                error_api = "Error al procesar la respuesta de la API."
    
    resultados_procesados = []
    if resultados_api:
        for anime_data in resultados_api:
            mal_id = anime_data.get('mal_id')
            if isinstance(mal_id, int): # Asegurarse que mal_id es un entero
                anime_data['es_favorito'] = mal_id in favoritos_ids
            else:
                anime_data['es_favorito'] = False # O manejar como error si es necesario
            resultados_procesados.append(anime_data)

    return render(request, 'anime_search.html', {
        'form': form,
        'resultados': resultados_procesados, # Usar los resultados procesados
        'error_api': error_api
    })

def toggle_favorito(request):
    if 'usuario_id' not in request.session:
        messages.error(request, 'Debes iniciar sesión para gestionar tus favoritos.')
        # Si es una petición AJAX en el futuro, podrías devolver un JSON de error.
        # Por ahora, redirigimos a login, aunque el formulario está en otra página.
        # Una mejor redirección sería a la página anterior si es posible.
        return redirect(request.META.get('HTTP_REFERER', 'login_usuario'))


    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión no es válida. Por favor, inicia sesión nuevamente.')
        return redirect(request.META.get('HTTP_REFERER', 'login_usuario'))

    if request.method == 'POST':
        anime_id_str = request.POST.get('anime_id')
        anime_titulo = request.POST.get('anime_titulo')

        if not anime_id_str or not anime_titulo:
            messages.error(request, 'Datos incompletos para marcar como favorito.')
            return redirect(request.META.get('HTTP_REFERER', 'buscar_anime'))

        try:
            anime_id = int(anime_id_str)
            
            favorito_existente, created = Favorito.objects.get_or_create(
                usuario=usuario,
                anime_id=anime_id,
                defaults={'anime_titulo': anime_titulo}
            )
            
            if created:
                messages.success(request, f'"{anime_titulo}" añadido a tus favoritos.')
            else:
                favorito_existente.delete()
                messages.info(request, f'"{anime_titulo}" eliminado de tus favoritos.')
                
        except ValueError:
            messages.error(request, 'ID de anime inválido.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            
        return redirect(request.META.get('HTTP_REFERER', 'buscar_anime'))

    # Si no es POST, redirigir a la página de búsqueda o a la anterior.
    return redirect(request.META.get('HTTP_REFERER', 'buscar_anime'))

def mis_favoritos(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para ver tus favoritos.')
        return redirect('login_usuario')
    try:
        current_user = Usuario.objects.get(id=request.session['usuario_id'])
        # Obtener los favoritos ordenados por fecha de adición (más recientes primero)
        favoritos = Favorito.objects.filter(usuario=current_user).order_by('-fecha_agregado')
    except Usuario.DoesNotExist:
        request.session.flush()
        messages.error(request, 'Tu sesión no es válida. Por favor, inicia sesión nuevamente.')
        return redirect('login_usuario')
    
    return render(request, 'mis_favoritos.html', {'favoritos': favoritos})