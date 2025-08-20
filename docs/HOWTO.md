# Habilitar un ambiente de desarrollo con Docker

Este documento describe cómo configurar y ejecutar un entorno de desarrollo para `deferia.cr` utilizando Docker.

> [!WARNING]
> Es ideal no saltarse pasos de esta guía, y de ser necesario, solicitar ayuda.

## Requisitos previos

### Windows

Es necesario tener instalados los siguientes componentes:

- [Windows Subsystem Linux](https://learn.microsoft.com/en-us/windows/wsl/setup/environment)
- [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Git](https://git-scm.com/downloads)


### Sistemas operativos basados en UNIX (MacOS, y distribuciones de Linux)

Es necesario tener instalados los siguientes componentes (se recomienda revisar la documentación específica del sistema operativo):

- [Python 3](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)


> [!TIP]
> Instalar [Docker Desktop](https://docs.docker.com/desktop/), incluye el engine de Docker y Docker Compose. Facilita visualizar los contenedores y brinda múltiples herramientas que pueden ser de utilidad.  


## Pasos a seguir previo a iniciar el contenedor

### 1. Clonar el repositorio

```bash
git clone https://github.com/tropicalizacion/ferias.git
```

### 2. Crear archivo de variables de entorno

Antes de iniciar el entorno, es necesario crear un archivo `.env` en la raíz del proyecto. Este archivo contiene variables sensibles como claves secretas y credenciales de base de datos.

> [!IMPORTANT]
> El archivo `.env` **no debe subirse** al repositorio. Solicite el contenido a otro colaborador del proyecto.

> [!NOTE]
> El archivo [`.env.example`](.env.example) tiene los campos que deben ser llenados.

### 3. Dar permisos a los _scripts_

Asegurarse que los _scripts_ sean ejecutables:

```bash
chmod +x ./scripts/*.sh
```

## Levantar el contenedor con el entorno de desarrollo

Según el sistema operativo, hay una distinción muy pequeña en el comando que se usa.

### Windows

Desde una terminal en la raíz del proyecto, levante el contenedor con el siguiente comando:

```bash
docker-compose up --build
```

### Sistemas operativos basados en UNIX (MacOS, y distribuciones de Linux)

Desde una terminal en la raíz del proyecto, levante el contenedor con el siguiente comando:

```bash
docker compose up --build
```

Este comando compilará la imagen (si es necesario) y levantará los servicios definidos en el `docker-compose.yml`. Esto puede tardar varios minutos en ejecutarse.

## Migraciones de la base de datos

Una vez que el contenedor esté corriendo correctamente, en una terminal nueva, ejecutar el _script_ necesario para las migraciones de la base de datos:

```bash
./scripts/dmigrations.sh
```

> [!NOTE]
> Es normal que se muestren varias advertencias durante este proceso

## Creacion de un usuario administrador

En caso de ser necesario, con el siguiente comando se puede llamar al script que es capaz de crear un usuario administrador para el entorno local:

```bash
./scripts/superuser.sh
```

## Acceso a la aplicación

Una vez que todo esté en funcionamiento, acceda al navegador con la siguiente dirección, que por defecto es el puerto 8000:

```
http://localhost:8000/
```

## Ejecución de comandos 

Como el proyecto se ejecuta por medio de Docker, en vez de usar un ambiente virtual de Python, es necesario realizar los comandos dentro del contenedor.

Ejemplo:

Para crear un usuario administrador, en un ambiente virtual de Python se usa el comando:

```bash
python manage.py createsuperuser
```

Mientras que en Docker, se usa el comando:

```bash
docker exec ferias_django_app python manage.py makemigrations
```


## Problemas comunes

### El contenedor no inicia o falla en la instalación

- Verificar que Docker esté corriendo correctamente.
- Asegurarse de que el archivo `.env` esté presente y correctamente configurado.
- Si se hacen cambios en el `Dockerfile` o en dependencias, ejecutar:

```bash
docker-compose down
docker-compose up --build
```

### El _script_ `dmigrations.sh` no funciona

- Asegurarse de haberle dado permisos de ejecución:

```bash
chmod +x ./scripts/dmigrations.sh
```

- Verificar que el contenedor esté activo antes de ejecutarlo.

## Otros comandos útiles

### Detener el entorno

```bash
docker-compose down
```

### Ver logs en tiempo real

```bash
docker-compose logs -f
```

### Abrir terminal Postgress

```bash
docker exec -ti postgres_db psql -U [USUARIO] -d ferias
```

---
