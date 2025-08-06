# Habilitar un ambiente de desarrollo con Docker

Este documento describe cómo configurar y ejecutar un entorno de desarrollo para deferia.cr con Django utilizando Docker.

- Usuario: `camote`
- Contraseña: `zanahoria`

## Requisitos previos

Es necesario tener instalados los siguientes componentes:

- [Python 3](https://www.python.org/)
- [Docker](https://www.docker.com/)

**Opcional pero útil**

- [Docker Desktop](https://docs.docker.com/desktop/)

## Configuración inicial

### 1. Clonar el repositorio

```bash
git clone https://github.com/tropicalizacion/ferias.git
```

### 2. Crear archivo de variables de entorno

Antes de iniciar el entorno, es necesario crear un archivo `.env` en la raíz del proyecto. Este archivo contiene variables sensibles como claves secretas y credenciales de base de datos.

> [!IMPORTANT]
> El archivo `.env` **no debe subirse** al repositorio. Solicite el contenido a otro colaborador del proyecto.

> [!NOTE]
> El archivo `.env.example` tiene los campos que deben ser llenados.

### 3. Dar permisos a los _scripts_

Asegurarse que los _scripts_ sean ejecutables:

```bash
chmod +x ./scripts/*.sh
```

## Levantar el entorno de desarrollo

Instalar `docker-compose`.

Para iniciar el contenedor de desarrollo:

```bash
docker-compose up --build
```

Este comando compilará la imagen (si es necesario) y levantará los servicios definidos en el `docker-compose.yml`. Este comando puede tardar varios minutos en ejecutarse.

## Migraciones de la base de datos

Una vez que el contenedor esté corriendo correctamente, en una terminal nueva, ejecutar el _script_ necesario para las migraciones de la base de datos:

```bash
./scripts/dmigrations.sh
```

Disclaimer: En primeras versiones se pueden mostrar

## Acceso a la aplicación

Una vez que todo esté en funcionamiento, acceda al navegador con la siguiente dirección, que por defecto es el puerto 8000:

```
http://localhost:8000/
```

## Sobre el archivo `.env`

Crear un nuevo archivo `.env` y agregar los siguientes campos siguiendo el formato de `.env.example`:

- `SECRET_KEY`:
- `DEBUG`:
- `DB_NAME`:
- `DB_USER`:
- `POSTGRES_PASSWORD`:
- `ALLOWED_HOSTS`:
- `DB_HOST`:
- `DB_PORT`:
- `GDAL_LIBRARY_PATH`:
- `GEOS_LIBRARY_PATH`:
- `GOOGLE_MAPS_API_KEY`:

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
