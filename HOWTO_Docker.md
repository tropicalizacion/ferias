# HOWTO: Habilitar un ambiente de desarrollo con Docker

Este documento describe cómo configurar y ejecutar un entorno de desarrollo para Ferias con Django utilizando Docker.

## Requisitos Previos

Es necesario tener instalados los siguientes componentes:

- [Python 3](https://www.python.org/)
- [Docker](https://www.docker.com/)

**Opcional pero útil**
- [Docker desktop](https://docs.docker.com/desktop/)

## Configuración Inicial

### 1. Clonar el repositorio

```bash
git clone https://github.com/tropicalizacion/ferias.git
```

### 2. Crear archivo de variables de entorno

Antes de iniciar el entorno, es necesario crear un archivo `.env` en la raíz del proyecto. Este archivo contiene variables sensibles como claves secretas y credenciales de base de datos.

**Importante:**  
El archivo `.env` **no debe subirse** al repositorio. Solicite el contenido a otro colaborador del proyecto.

### 3. Dar permisos a los scripts

Asegurarse que los scripts sean ejecutables:

```bash
chmod +x ./scripts/*.sh
```

## Levantar el Entorno de Desarrollo

Para iniciar el contenedor de desarrollo:

```bash
docker-compose up --build
```

Este comando compilará la imagen (si es necesario) y levantará los servicios definidos en el `docker-compose.yml`. Este comando puede tardar más de 2 minutos en ejecutarse.

## Migraciones de la Base de Datos

Una vez que el contenedor esté corriendo correctamente, en una terminal nueva, ejecutar el script necesario para las migraciones de la base de datos:

```bash
./scripts/dmigrations.sh
```


Disclaimer: En primeras versiones se pueden mostrar
## Acceso a la Aplicación

Una vez que todo esté en funcionamiento, accede al navegador con la siguiente dirección, que por defecto es el puerto 8000:

```
http://localhost:8000/
```

## Problemas Comunes

### El contenedor no inicia o falla en la instalación

- Verificar que Docker esté corriendo correctamente.
- Asegurarse de que el archivo `.env` esté presente y correctamente configurado.
- Si se hacen cambios en el `Dockerfile` o en dependencias, ejecutar:

```bash
docker-compose down
docker-compose up --build
```

### El script `dmigrations.sh` no funciona

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
