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
  - `product_id`: (AutoField) llave primaria.
  - `product_url`: (CharField) caracteres creados a partir del nombre común para usar en la URL. Ejemplo: https://feria.cr/productos/cebolla
  - ``
