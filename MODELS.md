# Modelos de la base de datos

Modelos según Django

## Ferias

- `class Marketplace`:
  - `marketplace_id`: (CharField) identificador único. Ejemplo: `curridabat`, `sansebastian`. Nota: este también será el URL de cada feria, por ejemplo: https://feria.cr/curridabat.

- `class Calendar`
  - `marketplace_id`: (ForeignKey:Feria.marketplace_id): llave foránea con las ferias.
  - `begins_day`: (IntegerField) día de la semana, 0: lunes, ..., 6: domingo.
  - `begins_time`: (TimeField) hora del día en que comienza.
  - `ends_day`: (IntegerField) día de la semana, 0: lunes, ..., 6: domingo.
  - `ends_time`: (TimeField) hora del día en que termina.

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
  - `common_name_variety`: (CharField) nombre común en Costa Rica de la variedad. Ejemplo: mecino.
  - `common_name_alternative`: (CharField) otros nombres comunes en Costa Rica de la variedad. Ejemplo: ácido.
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
