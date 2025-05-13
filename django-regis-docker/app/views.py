from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import csv
import os

def index(request):
    return HttpResponse("<h1>¡Hola, Django con Redis desde Docker!</h1>"
                       "<p>Esta aplicación está utilizando Redis como base de datos clave-valor.</p>"
                       "<p>Intenta usar los siguientes endpoints:</p>"
                       "<ul>"
                       "<li><a href='/get-all'>GET /get-all</a> - Ver todas las claves guardadas</li>"
                       "<li>POST /set - Establecer un valor (envía un JSON con 'key' y 'value')</li>"
                       "<li>GET /get?key=nombre_clave - Obtener un valor</li>"
                       "<li>DELETE /delete?key=nombre_clave - Eliminar un valor</li>"
                       "<li><a href='/load-products'>GET /load-products</a> - Cargar los primeros 10 productos del CSV</li>"
                       "<li><a href='/load-all-products'>GET /load-all-products</a> - Cargar todos los productos del CSV</li>"
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
    """Endpoint para obtener todas las claves guardadas"""
    # Obtener todas las claves con el prefijo 'product_'
    # Nota: En una implementación real con muchos productos, 
    # esto debería paginarse para evitar problemas de rendimiento
    
    # Intentamos obtener las claves de los productos usando un método indirecto
    # Redis no tiene una forma directa de obtener todas las claves a través de django-redis
    
    # Verificamos todas las claves que sabemos que existen (que han sido cargadas desde el CSV)
    products = {}
    product_keys = cache.get('product_keys', [])
    
    for key in product_keys:
        product = cache.get(key)
        if product is not None:
            products[key] = product
    
    return JsonResponse({'products': products})

@csrf_exempt
def delete_value(request):
    """Endpoint para eliminar un valor de Redis"""
    key = request.GET.get('key')
    
    if not key:
        return JsonResponse({'error': 'Parámetro key requerido'}, status=400)
    
    # Verificar si existe antes de eliminar
    if cache.get(key) is None:
        return JsonResponse({'error': f'La clave {key} no existe'}, status=404)
    
    # Si estamos eliminando un producto, también lo eliminamos de la lista de claves
    product_keys = cache.get('product_keys', [])
    if key in product_keys:
        product_keys.remove(key)
        cache.set('product_keys', product_keys)
    
    cache.delete(key)
    return JsonResponse({'status': 'success', 'message': f'Clave {key} eliminada correctamente'})

def load_products(request):
    """Cargar los primeros 10 productos del archivo CSV en Redis"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output.csv')
    
    try:
        products_loaded = 0
        product_keys = []
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            # Saltamos la fila del encabezado
            header = next(csv_reader)
            
            # Cargamos los primeros 10 productos
            for i, row in enumerate(csv_reader):
                if i >= 10:  # Limitamos a 10 productos
                    break
                
                if len(row) >= 13:  # Verificamos que la fila tenga suficientes columnas
                    product_data = {
                        'date': row[0],
                        'prod_id': row[1],
                        'prod_name': row[2],
                        'prod_name_long': row[3],
                        'prod_brand': row[4],
                        'category': row[5],
                        'subcategory': row[6],
                        'tags': row[7],
                        'prod_unit_price': row[8],
                        'prod_units': row[9],
                        'prod_icon': row[10],
                        'prod_source': row[11],
                        'source_type': row[12]
                    }
                    
                    # Usamos el prod_id como clave
                    key = row[1]
                    cache.set(key, product_data)
                    product_keys.append(key)
                    products_loaded += 1
        
        # Guardar las claves de los productos para poder recuperarlas después
        cache.set('product_keys', product_keys)
        
        return JsonResponse({
            'status': 'success', 
            'message': f'Se cargaron {products_loaded} productos', 
            'product_keys': product_keys
        })
        
    except FileNotFoundError:
        return JsonResponse({
            'error': f'No se encontró el archivo CSV en {csv_path}'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': f'Error al cargar productos: {str(e)}'
        }, status=500)

def load_all_products(request):
    """Cargar todos los productos del archivo CSV en Redis"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output.csv')
    
    try:
        products_loaded = 0
        product_keys = []
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            # Saltamos la fila del encabezado
            header = next(csv_reader)
            
            # Cargamos todos los productos
            for row in csv_reader:
                if len(row) >= 13:  # Verificamos que la fila tenga suficientes columnas
                    product_data = {
                        'date': row[0],
                        'prod_id': row[1],
                        'prod_name': row[2],
                        'prod_name_long': row[3],
                        'prod_brand': row[4],
                        'category': row[5],
                        'subcategory': row[6],
                        'tags': row[7],
                        'prod_unit_price': row[8],
                        'prod_units': row[9],
                        'prod_icon': row[10],
                        'prod_source': row[11],
                        'source_type': row[12]
                    }
                    
                    # Usamos el prod_id como clave
                    key = row[1]
                    cache.set(key, product_data)
                    product_keys.append(key)
                    products_loaded += 1
        
        # Guardar las claves de los productos para poder recuperarlas después
        cache.set('product_keys', product_keys)
        
        return JsonResponse({
            'status': 'success', 
            'message': f'Se cargaron {products_loaded} productos', 
            'product_keys': product_keys
        })
        
    except FileNotFoundError:
        return JsonResponse({
            'error': f'No se encontró el archivo CSV en {csv_path}'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': f'Error al cargar productos: {str(e)}'
        }, status=500)