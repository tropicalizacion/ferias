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

Se agrega el archivo `.env` al directorio ruta

(en caso de ser necesario) al descargar el archivo `.env` y pasarlo al directorio ruta puede salir como `.env.env` se
debe cambiar esto a solo `.env`

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
    - `/ferias/<código-de-ferias>`: información básica de la feria
    - `/ferias/buscar?param=valor`: resultados de la búsqueda de datos
- ***productos***
    - `/productos`: página de meta información sobre los datos que contiene la página
    - `/productos/<código-de-producto>`: editor de datos del producto elegido
- ***informacion***
    - `/informacion`: página de bienvenida a la sección de información
    - `/blog`, `/articulo`, etc.: otros sitios
- ***crowdsourcnig***
    - `/colaboracion`: página de bienvenida de la sección de colaboración colectiva
    - `/colaboracion/`:
- ***api***
    - `/api`: página de bienvenida e información sobre el API el proyecto
- ***usuarios***
    - `/usuarios`: página de información de usuarios
    - `/usuarios/perfil`: página de información de la persona usuaria
