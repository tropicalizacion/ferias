import pandas as pd

# leer csv
table = pd.read_csv("districts.csv")

# dividir el dataframe en dos, uno para los fields del JSON...
table_fields = table.drop(columns=["postal_code"])
table_fields = table_fields.transpose()

# ... y otro que contiene solo el model y el postal_code.
# insertar "model":"website.district" para cada distrito 
table.insert(0, "model", ["website.district" for x in range(table.shape[0])], True)
table = table[["model", "postal_code"]]

# renombrar "postal_code" a "pk"
table = table.rename(columns={"postal_code": "pk"})

# unir ambos dataframe para crear uno con tres columnas: model, postal_code y fields
table["fields"] = [table_fields[i].to_dict() for i in range(table.shape[0])]

# exportar dataframe a JSON
table.to_json("districts.json", orient="records")