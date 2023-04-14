# Ferias

> Sitio web con información de las ferias del agricultor en Costa Rica, en desarrollo por el trabajo comunal universitario TC-691 "Tropicalización de la Tecnología" de la Universidad de Costa Rica.

## Apps de Django

- `api`: API
- `crowdsourcing`: Crowdsourcing
- `datos`: Base de datos de las ferias
- `ferias`: Proyecto principal (donde está `settings.py`)
- `informacion`: Blogs y otras páginas de información general
- `productos`: Base de datos de los productos
- `sitio`: Página de inicio y otras páginas misceláneas (contacto, acerca de, etc.)
- `usuarios`: Manejo de usuarios

Tareas:

- [ ] Nuevo modelo de la base de datos 

### Principios para la clasificación en la base de datos

- Datos de las ferias: etiquetas de OpenStreetMaps
- Nombres científicos de los productos: APG IV
- Centros de origen de los productos: Vavilov
- Campos de los productos: etiquetas inventadas pero en el formato de OpenStreetMaps

## Cosas

- Que al construir una búsqueda con distintos criterios, se vaya formando una frase, tipo:

> Quiero una feria **cerca de mí** que esté **abierta el viernes**, que sea **mediana** y con **parqueo para bicicletas**

| **Buscar** |

donde las **palabras en negrita** son los criterios de búsqueda. 

- Que una frase al pie de página y de la campaña sea 

> Dulce abrigo y sustento nos da

:cry:
