# Ejemplos de Operaciones CRUD para Productos en Redis

Este documento proporciona ejemplos de cómo utilizar la API para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) con productos de supermercado usando Redis como base de datos clave-valor.

## Preparación

Antes de comenzar, asegúrate de que:

1. El proyecto está en ejecución con `docker-compose up`
2. El archivo `output.csv` está en la carpeta raíz del proyecto
3. Los endpoints están disponibles en http://localhost:8080

## 1. Cargar Productos desde CSV

### Cargar los primeros 10 productos

```
GET http://localhost:8080/load-products
```

Esto cargará los primeros 10 productos del archivo CSV en Redis.

### Cargar todos los productos

```
GET http://localhost:8080/load-all-products
```

Esto cargará todos los productos del archivo CSV en Redis.

## 2. Ver Todos los Productos

```
GET http://localhost:8080/get-all
```

Este endpoint muestra todos los productos almacenados en Redis.

## 3. Obtener un Producto Específico

```
GET http://localhost:8080/get?key=7702155021451
```

Esto recuperará el producto con ID "7702155021451" (Limpia tapicería en espuma Binner).

## 4. Crear/Actualizar un Producto

```
POST http://localhost:8080/set
Content-Type: application/json

{
  "key": "7702155099999",
  "value": {
    "date": "20230513",
    "prod_id": "7702155099999",
    "prod_name": "Producto Nuevo",
    "prod_name_long": "Descripción larga del producto nuevo",
    "prod_brand": "MARCA NUEVA",
    "category": "Supermercado",
    "subcategory": "Snacks",
    "tags": "Nuevo, Promoción",
    "prod_unit_price": "25.990",
    "prod_units": "Unidades",
    "prod_icon": "../icons/SVG/01-food/pizza.svg",
    "prod_source": "VERDE",
    "source_type": "1"
  }
}
```

Esto creará un nuevo producto en Redis o actualizará uno existente si la clave ya existe.

## 5. Eliminar un Producto

```
DELETE http://localhost:8080/delete?key=7702155099999
```

Esto eliminará el producto con ID "7702155099999" de Redis.

## Ejemplos con cURL

### Cargar productos
```bash
curl -X GET http://localhost:8080/load-products
```

### Ver todos los productos
```bash
curl -X GET http://localhost:8080/get-all
```

### Obtener un producto específico
```bash
curl -X GET http://localhost:8080/get?key=7702155021451
```

### Crear/Actualizar un producto
```bash
curl -X POST http://localhost:8080/set \
  -H "Content-Type: application/json" \
  -d '{
    "key": "7702155099999",
    "value": {
      "prod_id": "7702155099999", 
      "prod_name": "Producto Nuevo", 
      "prod_unit_price": "25.990"
    }
  }'
```

### Eliminar un producto
```bash
curl -X DELETE http://localhost:8080/delete?key=7702155099999
```

## Consejos para trabajar con productos

1. **Búsqueda por ID de producto**: Siempre usa el `prod_id` como clave para asegurar la unicidad.
2. **Actualización parcial**: Puedes actualizar solo algunos campos del producto usando el endpoint `set`.
3. **Formato de datos**: Asegúrate de mantener consistencia en los tipos de datos (especialmente en precios).
4. **Validación**: La API no valida la estructura de los datos, así que asegúrate de enviar datos correctos.