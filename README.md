# Ferias

Sitio web con información de las ferias del agricultor en Costa Rica, en desarrollo por el trabajo comunal universitario TC-691 "Tropicalización de la Tecnología" de la Universidad de Costa Rica.

## Descripción

Ferias es una plataforma integral que permite gestionar información detallada sobre ferias, productos y ubicaciones geográficas. El proyecto está diseñado para facilitar la colaboración colectiva (_crowdsourcing_) en la recopilación y mantenimiento de datos, ofreciendo una interfaz web intuitiva y un API público para desarrolladores.

## Características Principales

- Gestión Geoespacial: Integración con PostgreSQL + PostGIS para manejo de datos geográficos
- Base de Datos de Ferias: Catálogo completo de ferias con ubicaciones y detalles
- Catálogo de Productos: Sistema de gestión de productos ofrecidos en las ferias
- Crowdsourcing: Plataforma colaborativa para actualización de datos
- API Pública: Acceso programático a todos los datos del proyecto
- _Responsive_: Interfaz adaptable a diferentes dispositivos
- Búsqueda Avanzada: Búsquedas geoespaciales, por similitud y sin acentos
- Arquitectura del Sistema: El proyecto está estructurado en múltiples aplicaciones Django para una organización modular

## Apps de Django

- `ferias`: Proyecto principal (donde está `settings.py`)
- `marketplaces`: Base de datos de las ferias
- `products`: Base de datos de los productos
- `content`: Blogs y otras páginas de información general
- `website`: Página de inicio y otras páginas misceláneas (contacto, acerca de, etc.)
- `crowdsourcing`: Crowdsourcing
- `api`: API
- `users`: Manejo de usuarios

## Desarrollo

Para quienes desean colaborar en el proyecto, es necesario primero recibir aprobación de [Fabián Abarca](https://github.com/fabianabarca). Una vez conseguida la aprobación, porfavor revisar los siguientes archivos para habilitar un ambiente de desarrollo:

- [Habilitar un ambiente de desarrollo con Docker (recomendado)](docs/HOWTO.md)
- [Habilitar un ambiente de desarrollo de forma manual](docs/Manual_env.md)
