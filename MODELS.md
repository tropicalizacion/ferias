# Mapa del sitio

- Inicio
  - Ferias
    - Página de inicio de ferias específicamente con datos sobre las ferias en general
    - ...*cada feria*...
  - Productos
    - Página de inicio de productos específicamente con datos sobre los productos en general
    - ...*cada producto*...
    - Centros de origen
  - Consejos
    - Métodos de almacenamiento (#nutrición)
    - Métodos de preparación (#nutrición)
    - Consejos para la feria (cómo ir, etc.)
  - Blog (consejos, contenidos, información, cápsulas informativas, artículos) (mejorar SEO)
    - Los Cinco Preceptos (#ciencias-económicas y #nutrición)
    - Los precios de la feria (#ciencias-económicas)
    - ¿Por qué la gente prefiere ir a la feria? (#ciencias-económicas)
    - Frases vinculadas con vegetales y frutas ("no entiendo ni papa") (Angie de Filología)
    - Historia de las ferias (#comunicación-colectiva)
    - Anecdotario (*crowdsourced*) (#web-ferias, #comunicación-colectiva, #ciencias-económicas)
    - Travesía de una fresa, un día en la vida de un mango (#comunicación-colectiva, Marlon de Agronomía)
    - Sobre la gente que vende frutas y verduras (#comunicación-colectiva, #nutrición, Marlon)
    - Sobre la gente que **no** vende frutas y verduras (artesanías, productos procesados...) (#ciencias-económicas)
  - Anuncios (pizarra informativa)
  - Acerca de
    - Sobre el proyecto (quiénes somos)
    - Contacto

# Modelos de la base de datos

Modelos según Django

## Ferias

- `class Marketplace`:
  - `marketplace_url`: (CharField) identificador único. Ejemplo: `curridabat`, `sansebastian`. Nota: este también será el URL de cada feria, por ejemplo: https://feria.cr/curridabat.
  - `name`: (CharField) nombre común de la feria. No debe incluir "La Feria de..." y debe estar escrita con la ortografía correcta. Ejemplo: Tres Ríos.
  - `name_alternate`: (TextField) descripción de la feria.
  - `description`: (CharField)
  - `opening_hours`: (CharField) descripción de los horarios de apertura (según [referencia](https://wiki.openstreetmap.org/wiki/Key:opening_hours) de OpenStreetMaps). Ejemplo: "Mo-Fr 08:00-12:00,13:00-17:00. Nota: hay que evaluar la mejor forma de adaptar esto a partir de la tabla `Calendar` más adelante.
  - `location`: (PointField) ubicación SRID 4326 (WGS84) de la feria (GeoDjango).
  - `area`: (PolygonField) polígono que demarca el área o región donde está la feria (GeoDjango).
  - `size`: (CharField) nuestra propia clasificación del tamaño relativo de una feria, con los valores posibles:
    - S: pequeña
    - M: mediana
    - L: grande
    - XL: extra grande
  - `province`: (CharField) división provincial de Costa Rica.
  - `canton`: (CharField) división cantonal de Costa Rica.
  - `district`: (CharField) división distrital de Costa Rica.
  - `address`: (TextField) dirección "a la tica". Ejemplo: "En el gimnasio de la escuela de Guachipelín".
  - `phone`: (PhoneNumberField) número de teléfono (según recomendación [E.164](https://en.wikipedia.org/wiki/E.164) de UIT). Ejemplo: +50687654321.
  - `admin_committee`: (CharField) comité regional del CNP a la que pertenece la feria.
  - `admin_center`: (CharField) centro agrícola que administra la feria.
  - `email`: (EmailField) correo electrónico de contacto.
  - `website`: (URLField) dirección web de la feria (web, Facebook, etc.)
  - `products`: (ManyToMany) productos regulares en la oferta de la feria, vinculado con la tabla `Products`.
  - Infraestructura:
    - `parking`: (CharField)
    - `bicycle_parking`: (BooleanField)
    - `fairground`: (BooleanField)
    - `indoor`: (BooleanField)
    - `toilets`: (BooleanField)
    - `handwashing`: (BooleanField)
    - `drinking_water`: (BooleanField)
  - Servicios
    - `food`: (BooleanField)
    - `drinks`: (BooleanField)
    - `handicrafts`: (BooleanField)
    - `butcher`: (BooleanField)
    - `dairy`: (BooleanField)
    - `seafood`: (BooleanField)
    - `garden_centre`: (BooleanField)
    - `florist`: (BooleanField)
  - Otros
    - `payment`: (ManyToManyField)
    - `other_services`: (CharField)
  - Productos
    - `products`: (ManyToManyField)

- `class Photo`
  - `marketplace`: (ForeignKey(Marketplace))
  - `image`: (ImageField)
  - `description`: (CharField)
  - `profile`: (BooleanField)
  - `cover`: (BooleanField)

- `class Payment`
  - `name`: (CharField)

## Productos

- `class Product`
  - `product_id`: (AutoField) llave primaria, autogenerada.
  - `category`: (IntegerField) clasificación por categoría de planta comestible, donde:
    - 1: cereales
    - 2: legumbres
    - 3: frutas
    - 4: hortalizas
    - 5: condimentos  
  - `product_url`: (CharField) caracteres creados a partir del nombre común para usar en la URL. Ejemplo: https://feria.cr/productos/cebolla
  - `scientific_name`: (CharField) nomenclatura binomial según el Código Internacional de Nomenclatura. Ejemplo: Allium sativum.
  - `scientific_name_variety`: (CharField) variedad de una especie. Ejemplo: Allium ampeloprasum var. **porrum** (incluir solamente la variedad en este campo).
  - `common_name`: (CharField) nombre común en Costa Rica. Ejemplo: limón.
  - `common_name_variety`: (CharField) nombre común de la variedad en Costa Rica. Ejemplo: mecino.
  - `common_name_alternate`: (CharField) otros nombres comunes de la variedad en Costa Rica. Ejemplo: ácido.
  - `image`: (ImageField) imagen del producto.
  - `icon`: (FileField) icono para representar el producto en algunos lugares del sitio web.
  - `center_origin`: (IntegerField) centro de origen histórico del producto según la clasificación de Vavilov:
    - 1: (I) Asia oriental
    - 2: (II) Subcontinente indio
    - 3: (IIa) Archipiélago indo-malayo
    - 4: (III) Sureste y centro de Asia
    - 5: (IV) Asia Menor y Creciente Fértil
    - 6: (V) Mediterráneo
    - 7: (VI) Abisinia (actual Etiopía)
    - 8: (VII) Mesoamérica
    - 9: (VIII) Región andina tropical
    - 10: (VIIIa) Región chilena
    - 11: (VIIIb) Región brasileña-paraguaya
  - Nota: para cada mes a continuación existe la siguiente clasificación de estacionalidad:
    - 0: imposible o muy difícil de encontrar el producto
    - 1: producto escaso
    - 2: producto abundante
    - 3: plena temporada de cosecha
  - `jan`: (IntegerField) estacionalidad en enero.
  - `feb`: (IntegerField) estacionalidad en febrero.
  - `mar`: (IntegerField) estacionalidad en marzo.
  - `apr`: (IntegerField) estacionalidad en abril.
  - `may`: (IntegerField) estacionalidad en mayo.
  - `jun`: (IntegerField) estacionalidad en junio.
  - `jul`: (IntegerField) estacionalidad en julio.
  - `aug`: (IntegerField) estacionalidad en agosto.
  - `sep`: (IntegerField) estacionalidad en septiembre.
  - `oct`: (IntegerField) estacionalidad en octubre.
  - `nov`: (IntegerField) estacionalidad en noviembre.
  - `dec`: (IntegerField) estacionalidad en diciembre.
  - `nutritional_description`: (TextField) comentario sobre su valor nutricional.

- `class Preparation`
  - `product_id`: (ForeignKey) llave foránea con la tabla de productos.
  - `method`: (IntegerField) selección de una lista de métodos de preparación de alimentos:
    - 1: hervir
  - `recommendation`: (IntegerField) nivel de recomendación (?):
    - 1: preparación más saludable
    - 2: no sé qué
  - `description`: (TextField) descripción del método con este producto.

- `class Storage`
  - `product_id`: (ForeignKey) llave foránea con la tabla de productos.
  - `method`: (IntegerField) selección de una lista de métodos de almacenamiento de alimentos:
    - 1: a temperatura ambiente
    - 2: refrigerar
    - 3: congelar
  - `recommendation`: (IntegerField) nivel de recomendación (?):
    - 1: preparación más saludable
    - 2: no sé qué
  - `description`: (TextField) descripción del método con este producto.
