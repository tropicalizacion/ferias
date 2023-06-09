# TCU tropicalización de la tecnología 
# Mike Mai Chen
# script que convierte datos tabulados en un archivo en formato
# JSON para la base de datos con las variedades de los productos
# que ofrecen las ferias

import pandas

# leer csv y quitar todas las filas que no tenga un variety_id
table = pandas.read_csv("products_variety.csv")
table = table[table["variety_id"].notnull()]

# dividir el dataframe en dos, uno para los fields del JSON...
table_fields = table.drop(columns=["variety_id"])
table_fields = table_fields.transpose()

# ... y otro que contiene solo el model y el variety_id.
# insertar "model":"products.variety" para cada producto
table.insert(0, "model", ["products.variety" for x in range(table.shape[0])], True)
table = table[["model", "variety_id"]]

# unir ambos dataframe para crear uno con tres columnas: model, variety_id y fields
table["fields"] = [table_fields[i].to_dict() for i in range(table.shape[0])]

# exportar dataframe a JSON
table.to_json("products_variety.json", orient="records")