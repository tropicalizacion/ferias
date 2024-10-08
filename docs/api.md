# De Feria API

## Funcionamiento

### Workflow

Como se está utilizando Django Rest Framework, se va a seguir la estructura de la API que se describe en la documentación de [DRF]("https://www.django-rest-framework.org/tutorial/quickstart/"). Todo empieza en el modelo de la aplicación, que se va a definir en el archivo `models.py`. Luego, se va a crear un serializador en el archivo `serializers.py` que va a convertir los objetos de la base de datos en JSON. En este serializador se pueden escoger y dar formato a los datos que se quieren mostrar, por ejemplo, omitir algunos campos del modelo o empotrar datos de un modelo dentro del serializador de otro. Por último, se va a crear una vista en el archivo `views.py` que va a definir cómo se va a ver la información en la API. Estas vistas se implementan mediante viewsets, que son clases que definen cómo se van a ver los datos en la API. Por último, se va a definir la URL de la API en el archivo `urls.py` de la aplicación.

### Documentación de la API

La documentación de la API se va a generar automáticamente con la librería `spectacular` y `redoc`. La librería `spectacular` va a generar la documentación de la API en formato JSON y `redoc` va a mostrar la documentación en un formato más amigable. Para que esto suceda, `spectacular` debe generar un esquema de la API y `redoc` debe leer este esquema y mostrarlo en la URL `/api/docs/`. La información autogenerada por `spectacular` se puede modificar en el archivo `settings.py` en la sección `SPECTACULAR_SETTINGS`, o bien, (de forma más segura) utilizando la librería `extend_schema`, para añadir descripciones y mejorar la legibilidad de los métodos básicos de la API (list, create, retrieve, update, partial update, delete).

### Actualización y generación de la documentación

Existen limitaciones en la generación de la documentación de la API. Por ejemplo, no se pueden añadir títulos para la API o descripciones y licencias de la misma. Para solucionar esto, se ha decidio utilizar un documento .yaml que va a contener información estática sobre la API. Este documento se va a utilizar para generar el esquema definitivo que utilizará Redoc para mostrar la documentación. 

Para actualizar la documentación autogenerada, se debe correr este comando:

```bash
python manage.py spectacular --color --file api/schema.yml
```

Esto escribe el esquema autogenerado por `spectacular` en el archivo `api/schema.yml`. Luego, se debe ejecutar el comando:

```bash
python api/comb_schema_script.py
```

Este script combina el esquema autogenerado por `spectacular` con el esquema estático que se encuentra en el archivo `api/schema_static.yml`. Este archivo contiene información sobre la API que no se puede autogenerar, como títulos, descripciones y licencias. El script combina estos dos archivos y escribe el esquema definitivo en el archivo `api/schema.yml`. Por último, se debe correr el servidor y acceder a la URL `/api/docs/` para ver la documentación de la API.

## Ferias

Esta API va a permitir a los usuarios ver y (en caso de tener los permisos) modificar la información sobre las ferias. El formato esperado de esta API es el siguiente:

```json
{
    "url": "http://127.0.0.1:8000/datos/api/ferias/alajuela/",
    "name": "Alajuela",
    "opening_hours": "Fr 12:00-20:00; Sa 06:00-13:00",
    "location": {
        "type": "Point",
        "coordinates": [
            -84.2190568571068,
            10.013534238571
        ]
    },
    "size": "XL",
    "province": "Alajuela",
    "canton": "Alajuela",
    "district": "Alajuela",
    "postal_code": 20101,
    "address": "en Plaza Ferias. De la bomba Santa Anita, 200 m al oeste. Del PriceSmart de Alajuela, 250 m al este. Por Ekono",
    "phone": 24432010,
    "email": "pferias@plazaferias.com",
    "website": null,
    "facebook": "https://www.facebook.com/people/Plaza-Ferias-Alajuela/100064584170065/",
    "instagram": null,
    "opening_date": null,
    "operator": "Plaza Ferias",
    "branch": null,
    "type": "mercado",
    "parking": "surface",
    "bicycle_parking": true,
    "fairground": true,
    "indoor": true,
    "toilets": true,
    "handwashing": true,
    "drinking_water": true,
    "food": true,
    "drinks": true,
    "handicrafts": true,
    "butcher": true,
    "dairy": true,
    "seafood": true,
    "spices": null,
    "garden_centre": true,
    "florist": true,
    "other_services": null
}
```

Todos los atributos pueden estar en blanco o ser nulos excepto `url` (llave primaria), `name`, `province`, `canton` y `district`.

## GeoFerias

Este API trata con los datos relativos a las ubicaciones de las ferias. Su objetivo es retornar un archivo geojson en lugar de un json normal. Esto porque el geojson se utiliza para tratar con datos geométricos y en este caso, geográficos. El formato esperado de esta API es el siguiente:

```json
{
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [
            -84.2190568571068,
            10.013534238571
        ]
    },
    "properties": {
        "name": "Alajuela",
        "province": "Alajuela",
        "canton": "Alajuela",
        "district": "Alajuela",
        "postal_code": 20101,
        "address": "en Plaza Ferias. De la bomba Santa Anita, 200 m al oeste. Del PriceSmart de Alajuela, 250 m al este. Por Ekono"
    }
}
```

Tiene los mismos atributos no nulos que la API de ferias, pero en este caso, se añade un atributo `geometry` que contiene la información de la ubicación de la feria. Este es el atributo `location` en el modelo original y puede ser nulo, por lo que se debe tener esto en cuenta y manejar el caso en el futuro.

## Productos

Este API trata con los diferentes tipos de productos que se pueden encontrar en las diferentes ferias a lo largo del país. Cada producto tiene asociado una variedad, dicha variedad puede tener nombre científico, nombre común, disponibilidad por temporada, entre otros. El formato esperado de esta API es el siguiente:

```json
{
    "product_url": "acelga",
    "category": "verdura",
    "common_name": "acelga",
    "common_name_alternate": null,
    "description": "La acelga, al igual que la espinaca, brilla en ensaladas, pues aporta frescura y un inmenso valor nutricional. Reconocida por su alto aporte en minerales y vitaminas esenciales, es la adición perfecta para una dieta equilibrada.",
    "name_origin": null,
    "center_origin": [
        "VI"
    ],
    "center_origin_notes": "La cocina etíope, rica en opciones vegetarianas, ha visto nacer a la acelga en sus tierras y ha sido la primera en acogerla como un ingrediente esencial en sus deliciosas recetas verdes.",
    "food_basket": false,
    "nutrition_notes": "La acelga, rica en vitaminas A, C y K y minerales esenciales para el buen funcionamiento del organismo, como magnesio, hierro y potasio, también ayuda a regular los procesos digestivos. Su elevado contenido de vitamina K ayuda a mantener sanos los huesos y la sangre.",
    "preparation": [],
    "preparation_notes": null,
    "storage": [],
    "storage_notes": "En un recipiente cerrado con poca humedad",
    "varieties": [
        {
            "common_name_variety": null,
            "scientific_name": "Beta vulgaris",
            "scientific_name_variety": "cicla",
            "common_name_variety_alternate": null,
            "jan": 3,
            "feb": 3,
            "mar": 3,
            "apr": 2,
            "may": 2,
            "jun": 2,
            "jul": 2,
            "aug": 1,
            "sep": 1,
            "oct": 2,
            "nov": 2,
            "dec": 2
        }
    ]
}
```

En este caso, los atribbutos que no pueden ser nullos son product_url, category, common name y variety_id, en el caso del modelo de variedades.

## Precios

```json
{
    "product" = "aguacate Hass"
    "prices-history" = [
        
    ]
}
```
