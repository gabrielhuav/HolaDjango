from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return HttpResponse("<h1>¡Hola, Django con Redis desde Docker!</h1>"
                       "<p>Esta aplicación está utilizando Redis como base de datos clave-valor.</p>"
                       "<p>Intenta usar los siguientes endpoints:</p>"
                       "<ul>"
                       "<li><a href='/get-all'>GET /get-all</a> - Ver todas las claves guardadas</li>"
                       "<li>POST /set - Establecer un valor (envía un JSON con 'key' y 'value')</li>"
                       "<li>GET /get?key=nombre_clave - Obtener un valor</li>"
                       "<li>DELETE /delete?key=nombre_clave - Eliminar un valor</li>"
                       "</ul>")

@csrf_exempt
def set_value(request):
    """Endpoint para establecer un valor en Redis"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            key = data.get('key')
            value = data.get('value')
            
            if not key:
                return JsonResponse({'error': 'La clave es requerida'}, status=400)
            
            # Guardar en Redis
            cache.set(key, value)
            return JsonResponse({'status': 'success', 'message': f'Valor para {key} guardado correctamente'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def get_value(request):
    """Endpoint para obtener un valor de Redis"""
    key = request.GET.get('key')
    
    if not key:
        return JsonResponse({'error': 'Parámetro key requerido'}, status=400)
    
    value = cache.get(key)
    
    if value is None:
        return JsonResponse({'error': f'La clave {key} no existe'}, status=404)
    
    return JsonResponse({'key': key, 'value': value})

def get_all_keys(request):
    """Endpoint para obtener todas las claves guardadas (demostrativo)"""
    # Este es un método simplificado para ver las claves
    # En un ambiente de producción necesitarías usar Redis directamente
    # ya que django-redis no provee una forma directa de obtener todas las claves
    
    # Aquí usamos un workaround - si tienes algunas claves predefinidas para probar
    test_keys = ["key1", "key2", "key3", "user1", "user2", "product1"]
    
    results = {}
    for key in test_keys:
        value = cache.get(key)
        if value is not None:
            results[key] = value
    
    # También mostramos cualquier otra clave que se haya creado durante la sesión
    # (esto solo funciona para claves que sabemos que existen)
    
    return JsonResponse({'keys': results})

@csrf_exempt
def delete_value(request):
    """Endpoint para eliminar un valor de Redis"""
    key = request.GET.get('key')
    
    if not key:
        return JsonResponse({'error': 'Parámetro key requerido'}, status=400)
    
    # Verificar si existe antes de eliminar
    if cache.get(key) is None:
        return JsonResponse({'error': f'La clave {key} no existe'}, status=404)
    
    cache.delete(key)
    return JsonResponse({'status': 'success', 'message': f'Clave {key} eliminada correctamente'})