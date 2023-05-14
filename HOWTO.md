# Configuración del sitio

## Clave secreta de Django

La clave secreta de Django y otras configuraciones están en un archivo `.env` y es manipulado por el paquete `python-decouple` ([documentación](https://pypi.org/project/python-decouple/)).

Para iniciar:

```bash
pip install python-decouple
```

Agregar: en `editor/settings.py`:

```python
from decouple import config
```

Se agrega el archivo `.env` al directorio raíz. Nota: (en caso de ser necesario) al descargar el archivo `.env` y pasarlo al directorio raíz puede salir como `.env.env` se debe cambiar esto a solo `.env`.

(Seguir instrucciones de la documentación).

> El equipo de desarrolladores compartirá el documento `.env`.

Luego, se deben instalar los siguientes paquetes:

```bash
`pip install django`
```

```bash
`pip install bootstrap-py`
```

Por último, Para ejecutar el proyecto se utiliza el comando:

```bash
`python manage.py runserver`
```

Para acceder al sitio en desarrollo se realiza mediante localhost en el puerto seleccionado

## Migrar a GeoDjango

[GeoDjango](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/) será utilizado con PostgreSQL y PostGIS.

- Instalar PostgreSQL.
- Instalar PostGIS.
- Crear base de datos `ferias` con `$ createdb ferias`.
- Ingresar con `$ psql ferias`.
- [Habilitar PostGIS](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/postgis/) para la base de datos `ferias` con `# CREATE EXTENSION postgis;`.
- Modificar `settings.py` con (asumiendo que la DB no tiene password):
```python
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": config('DB_NAME'),
        "USER": config('DB_USER'),
    },
}
```
y con:
```python
INSTALLED_APPS = [
    (...)
    "django.contrib.gis",
]
```
- Agregar a `.env` (asumiendo que el usuario de PostgreSQL es `postgres`, y si no lo sabe puede hacer en psql: `# SELECT current_user;`):
```
DB_NAME=ferias
DB_USER=postgres
```
- (Opcional) En algunos sistemas operativos, es necesario adjuntar a `settings.py`:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": config('DB_NAME'),
        "USER": config('DB_USER'),
    },
}

GDAL_LIBRARY_PATH = config('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = config('GEOS_LIBRARY_PATH')
```
y en `.env`:
```
GDAL_LIBRARY_PATH=/opt/homebrew/opt/gdal/lib/libgdal.dylib
GEOS_LIBRARY_PATH=/opt/homebrew/opt/geos/lib/libgeos_c.dylib
```
o lo que corresponda.
- Hacer todas las migraciones con `$ python manage.py makemigrations marketplaces` y así para cada app (products, website, etc.)
- Migrar con `$ python manage.py migrate` para crear las tablas.
- Hacer `$ python manage.py loaddata auth` para cargar los datos de usuarios de prueba del fixture (peligroso).

Con esto debería funcionar la aplicación pero ahora con PostgreSQL y PostGIS activado para usar GeoDjango, que permite guardar ubicaciones y regiones en el mapa y hacer búsquedas geoespaciales.

## Aplicaciones del sitio

Django utiliza "apps" para manejar el sitio. Por experiencia, sabemos que son divisiones útiles para la organización del sitio, aunque realmente desde una sola app se podrían realizar todas las funciones. Por orden, sin embargo, es mejor hacer una separación funcional. En ese sentido, y con base en la funcionalidad esperada del sitio, se han creado los siguientes apps:

<dl>
    <dt>sitio</dt>
    <dd>Administra páginas generales, como el "index", acerca de, contacto, etc.</dd>
    <dt>datos</dt>
    <dd>Administra la base de datos de ferias.</dd>
    <dt>productos</dt>
    <dd>Administra la base de datos de productos ofrecidos en las ferias.</dd>
    <dt>informacion</dt>
    <dd>Administra las páginas de información para visitantes, como blogs, tutoriales, etc.</dd>
    <dt>crowdsourcing</dt>
    <dd>Administra la colaboración colectiva para el mantenimiento y actualización de datos de las ferias y productos.</dd>
    <dt>api</dt>
    <dd>Administra un API público para que cualquier persona recopile datos de este proyecto.</dd>
    <dt>usuarios</dt>
    <dd>Administra los distintos tipos de usuarios del sitio.</dd>
</dl>

## Páginas del sitio

Con base en la funcionalidad descrita, es posible crear un primer esbozo de las páginas que tendrá el sitio (arquitectura de información), clasificadas según el app que las gestiona:

- ***sitio***
    - `/`: página de bienvenida
    - `/acerca`, `/contacto`, etc.: información sobre el sitio web
- ***datos***
    - `/ferias`: página de meta información sobre los datos que contiene la página
    - `/ferias/<código-de-feria>`: información básica de la feria
    - `/ferias/<código-de-feria>/edicion`: edición de la información
- ***productos***
    - `/productos`: página de meta información sobre los datos que contiene la página
    - `/productos/<código-de-producto>`: editor de datos del producto elegido
- ***informacion***
    - `/informacion`: página de bienvenida a la sección de información
    - `/blog`, `/articulo`, etc.: otros sitios
- ***crowdsourcing***
    - `/colaboracion`: página de bienvenida de la sección de colaboración colectiva
    - `/colaboracion/`:
- ***api***
    - `/api`: página de bienvenida e información sobre el API el proyecto
- ***usuarios***
    - `/usuarios`: página de información de usuarios
    - `/usuarios/perfil`: página de información de la persona usuaria

### Mapa del sitio

```mermaid
stateDiagram-v2
    por : Portada
    fer : Ferias
    feX : Cada feria
    fed : Editar info
    pro : Productos
    prX : Cada producto
    inf : Información
    blo : Blog
    cro : Crowdsourcing
    api : API
    ace : Acerca de
    reg : Registro
    ing : Ingreso
    ini : Inicio
    per : Perfil
    edi : Ediciones
    state log <<choice>>
    state usu <<choice>>
    state men <<fork>>

    [*] --> por
    por --> fer
    fer --> feX
    feX --> fed
    por --> pro
    pro --> prX
    por --> inf
    inf --> blo
    inf --> cro
    inf --> api
    por --> ace
    por --> log
    log --> ini : Logueado
    log --> usu : No logueado
    usu --> ing : Registrado
    usu --> reg : No registrado
    ing --> ini
    reg --> ing
    ini --> men
    men --> per
    men --> edi
```
