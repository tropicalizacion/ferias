import yaml

# Cargar el esquema autogenerado
with open('api/schema.yml', 'r') as file:
    schema = yaml.safe_load(file)

# Cargar el archivo YAML estático
with open('api/static_schema.yml', 'r') as file:
    static_data = yaml.safe_load(file)

# Combinar ambos
combined_schema = {**schema, **static_data}

# Guardar el esquema combinado
with open('api/schema.yml', 'w') as file:
    yaml.dump(combined_schema, file)
