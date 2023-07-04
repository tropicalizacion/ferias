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
  - `product_url`: (CharField) llave primaria, caracteres creados a partir del nombre común para usar en la URL. Ejemplo: https://feria.cr/productos/cebolla.
  - `common_name`: (CharField) nombre común en Costa Rica. Ejemplo: limón.
  - `common_name_alternate`: (CharField) otros nombres comunes de la variedad en Costa Rica. Ejemplo: ácido.
  - `category`: (CharField) clasificación por categoría de planta comestible, donde:
    - hortaliza: Hortaliza (verdura)
    - fruta: Fruta
    - cereal: Cereal (grano)
    - legumbre: Legumbre (leguminosa)
    - tubérculo: Tubérculo o raíz
    - condimento: Condimento (especia)
    - otro: Otra categoría
  - `description`: (TextField) descripción del producto.
  - `icon`: (ImageField) icono para representar el producto en algunos lugares del sitio web.
  - `food_basket`: (BooleanField) indica si el producto es parte de la canasta básica.
  - `nutrition_notes`: (TextField) información nutricional.
  - `preparation`: (ManyToManyField) formas de preparar el producto.
  - `preparation_notes`: (TextField) comentarios sobre las formas de preparación.
  - `storage`: (ManyToManyField) formas de almacenar el producto.
  - `storage_notes`: (TextField) comentarios sobre las formas de almacenamiento.
  - `center_origin`: (ManyToManyField) centro de origen histórico del producto.
  - `center_origin_notes`: (TextField) comentarios sobre el centro de origen.

- `class Variety`
  - `variey_id`: (AutoField) llave primaria, autogenerada.
  - `product_url`: (ForeingKey) llave foránea con la tabla de productos.
  - `scientific_name`: (CharField) nomenclatura binomial según el Código Internacional de Nomenclatura. Ejemplo: Allium sativum.
  - `scientific_name_variety`: (CharField) variedad de una especie. Ejemplo: Allium ampeloprasum var. **porrum** (incluir solamente la variedad en este campo).
  - `common_name_variety`: (CharField) nombre común de la variedad en Costa Rica. Ejemplo: mecino.
  - `common_name_variety_alternate`: (CharField) nombre común alternativo de la variedad en Costa Rica.
  - `description`: (TextField) descripción de la variedad.
  - `image`: (ImageField) imagen de la variedad.
  - Nota: para cada mes a continuación existe la siguiente clasificación de estacionalidad:
    - 0: Sin disponibilidad
    - 1: Poca disponibilidad
    - 2: Buena disponibilidad
    - 3: Temporada alta
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

- `class Origin`
  - `code`: (CharField) llave primaria, código del centro de origen según Vavilov.
  - `name`: (CharField) nombre del centro de origen según Vavilov.
  - `description`: (TextField) descripción del centro de origen.
  - `region`: (PolygonField) información geoespacial del centro de origen según Vavilov.

- `class Preparation`
  - `preparation_url`: (CharField) llave primaria, caracteres creados a partir de la preparación para usar en la URL.
  - `method_name`: (CharField) Nombre de la forma de preparación.
  - `method_description`: (TextField) descripción del método de preparación.
- `icon`: (ImageField) icono para representar la forma de preparación en algunos lugares del sitio web.

- `class Storage`
  - `storage_url`: (CharField) llave primaria, caracteres creados a partir de la almacenamiento para usar en la URL.
  - `method_name`: (CharField) Nombre de la forma de almacenamiento.
  - `method_description`: (TextField) descripción del método de almacenamiento.
- `icon`: (ImageField) icono para representar la forma de almacenamiento en algunos lugares del sitio web.