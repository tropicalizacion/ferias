# TCU tropicalización de la tecnología 
# Mike Mai Chen
# script que convierte datos tabulados en un archivo en formato
# JSON para la base de datos con información de los productos que
# ofrecen las ferias del agricultor

import pandas

# leer csv y acondicionar dataframe
table = pandas.read_csv("products_product.csv")

# elimina todas las filas que no tengan
# un pk y columnas ACTUALIZAR
table.rename(columns={"product_url":"pk"}, inplace=True)
table = table[table["pk"].notnull()]

# convertir la columna center_origin de string a lista
table["center_origin"] = table["center_origin"].str.split(", ")

# convertir las columnas storage y preparation de null a lista vacías
table["storage"] = [[] for x in range(table.shape[0])]
table["preparation"] = [[] for x in range(table.shape[0])]

# dividir el dataframe en dos, uno para los fields del JSON...
table_fields = table.drop(columns=["pk"])
table_fields = table_fields.transpose()

# ... y otro que contiene solo el model y el product_url.
# insertar "model":"products.product" para cada producto 
table.insert(0, "model", ["products.product" for x in range(table.shape[0])], True)
table = table[["model", "pk"]]

# unir ambos dataframe para crear uno con tres columnas: model, marketplace_url y fields
table["fields"] = [table_fields[i].to_dict() for i in range(table.shape[0])]

# exportar dataframe a JSON
table.to_json("products_product.json", orient="records")