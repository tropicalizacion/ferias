# Configuración del sitio

Este documento tiene la principal funcionalidad de proporcionar una guía para la ejecución del proyecto. Con esto se pretende mejorar su mantenibilidad y desarrollo de futuras funcionalidades.

## Paso 1. Clone el repositorio en su computadora

Puede hacerlo con HTTPS o SSH. Luego de clonar el repositorio, ábralo desde su ambiente de desarrollo seleccionado.

## Paso 2. Clave secreta de Django

La clave secreta de Django y otras configuraciones están en un archivo `.env` y es manipulado por el paquete `python-decouple` ([documentación](https://pypi.org/project/python-decouple/)).
Para obtener el archivo `.env` por favor ponerse en contacto con el profesor o desarrollador encargado.

Al obtener el archivo `.env`, colóquelo en el directorio root del proyecto.

## Paso 3. Instalación `pip`

Para, iniciar se debe instalar `pip`. Este es el instalador de paquetes que se utiliza python y será necesario para todas las librerías y paquetes que se utilizan en este proyecto. Para su instalación, inicie una terminal dentro del proyecto y ejecute los siguientes comandos: `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` y luego `python get-pip.py`. ([documentación](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/))

## Paso 4. Instalación de paquetes y librerías

Instale los siguientes paquetes con `pip`:

```bash
pip install django
```

```bash
pip install python-decouple
```

```bash
pip install bootstrap-py
```

```bash
pip install Pillow
```

## Paso 5. Migrar a GeoDjango

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
- Para ver mapas de OpenStreetMap en el panel de administración, hay que editar `marketplaces/admin.py` con:
```python
from django.contrib.gis import admin
(...)
admin.site.register(Marketplace, admin.GISModelAdmin)
```

En caso de tener problemas con la instalación de este paso en windows o en ubuntu, consultar la siguiente [documentación](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04)

Con esto debería funcionar la aplicación pero ahora con PostgreSQL y PostGIS activado para usar GeoDjango, que permite guardar ubicaciones y regiones en el mapa y hacer búsquedas geoespaciales.

## Paso 6. Ejecución del proyecto

Por último, Para ejecutar el proyecto se utiliza el comando:

```bash
python manage.py runserver
```

Para acceder al sitio en desarrollo se realiza mediante localhost en el puerto seleccionado

## Procedimiento para la actualización del repositorio en el servidor:

Si luego de un cambio en el repositorio se desea subir estos al sitio web, se debe realizar lo siguiente:

- Acceder remotamente el servidor con SSH ```bash ssh tcu@[IP DeFerias] ``` o vía el Access Console de Digital Ocean (en este caso hay que cambiar al usuario “tcu” con su tcu)
- En la terminal, moverse a ```bash cd ~/ferias ```
- Hacer ```bash git pull ``` en la rama que corresponde
- Reiniciar Nginx y Gunicorn con: ```bash sudo systemctl restart nginx ``` y ```bash sudo systemctl restart gunicorn ```
- Si hay que hacer migraciones de la base de datos entonces hay que entrar al ambiente virtual con ```bash source feriasenv/bin/activate ``` que es donde existe Python, Django y todos los paquetes asociados
- Antes de subir los cambios revisar que todo funcione de manera correcta y tener cuidado con las migraciones

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
