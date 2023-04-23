# Ferias

> Sitio web con información de las ferias del agricultor en Costa Rica, en desarrollo por el trabajo comunal universitario TC-691 "Tropicalización de la Tecnología" de la Universidad de Costa Rica.

## Apps de Django

- `ferias`: Proyecto principal (donde está `settings.py`)
- `marketplaces`: Base de datos de las ferias
- `products`: Base de datos de los productos
- `content`: Blogs y otras páginas de información general
- `website`: Página de inicio y otras páginas misceláneas (contacto, acerca de, etc.)
- `crowdsourcing`: Crowdsourcing
- `api`: API
- `users`: Manejo de usuarios

### Principios para la clasificación en la base de datos

- Datos de las ferias: etiquetas de OpenStreetMaps
- Nombres científicos de los productos: APG IV
- Centros de origen de los productos: Vavilov
- Campos de los productos: etiquetas inventadas pero en el formato de OpenStreetMaps

## Cosas

- Que al construir una búsqueda con distintos criterios, se vaya formando una frase, tipo:

> Quiero una feria **cerca de mí** que esté **abierta el viernes en la tarde**, que sea **mediana** y con **parqueo para bicicletas**

| **Buscar** |

donde las **palabras en negrita** son los criterios de búsqueda. ¿Por qué esta frase? No deja dudas sobre lo que está buscando. (Algún día puede ser un dictado del usuario + NLP).

Los criterios de búsqueda se pueden clasificar en cuatro: por **ubicación** ("cerca de mí", "cerca de X"), por **horario** ("abierto lunes en la mañana", "abierto viernes en la tarde"), por **características** ("que sea mediana", "que esté bajo techo"), y por **amenidades** ("con parqueo", "con comidas").

- La búsqueda debe resolver resultados aproximados y/o recomendados, es decir, que cumplan con la mayoría de características

- Que una frase al pie de página y de la campaña sea 

> Dulce abrigo y sustento nos da

:cry:
