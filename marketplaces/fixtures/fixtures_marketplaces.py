# TCU tropicalización de la tecnología 
# Mike Mai Chen
# script que convierte datos tabulados en un archivo en formato
# JSON para la base de datos con información de las ferias del agricultor

import pandas

# leer csv y quitar todas las filas que no tenga un marketplace_url
table = pandas.read_csv("marketplaces.csv")
table = table[table["marketplace_url"].notnull()]

# dividir el dataframe en dos, uno para los fields del JSON...
table_fields = table.drop(columns=["marketplace_url"])
table_fields = table_fields.transpose()

# ... y otro que contiene solo el model y el marketplace_url.
# insertar "model":"marketplaces.marketplace" para cada feria 
table.insert(0, "model", ["marketplaces.marketplace" for x in range(table.shape[0])], True)
table = table[["model", "marketplace_url"]]

# renombrar "marketplace_url" a "pk"
table = table.rename(columns={"marketplace_url": "pk"})

# unir ambos dataframe para crear uno con tres columnas: model, marketplace_url y fields
table["fields"] = [table_fields[i].to_dict() for i in range(table.shape[0])]

# exportar dataframe a JSON
table.to_json("marketplaces.json", orient="records")