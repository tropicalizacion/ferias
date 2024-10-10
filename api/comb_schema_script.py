import yaml

# TODO: Añadir el esquema autogenerado de redoc y no volver a cargarlo
# todo otra vez. Revisar "https://www.django-rest-framework.org/api-guide/schemas/"

# In order for the schema to be generated correctly, use the following command:
# `./manage.py spectacular --color --file schema.yml`
# this will write the auto generated to the file `schema.yml`
# and then run this script to combine the auto generated schema with the static schema


# Load the auto generated schema
with open('api/schema.yml', 'r') as file:
    schema = yaml.safe_load(file)

# Load the static schema
with open('api/static_schema.yml', 'r') as file:
    static_data = yaml.safe_load(file)

# Combine the two schemas
combined_schema = {**schema, **static_data}

# Save the combined schema
with open('api/schema.yml', 'w') as file:
    yaml.dump(combined_schema, file)
