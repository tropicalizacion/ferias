import csv
import json
from datetime import datetime
from uuid import uuid4

EXCLUDED_PRODUCTS = {"huevos", "queso_tipo_turrialba", "dulce", "hongos_frescos", "manga_grande_keitt", "manga_grande_tommy", "manga_pequena_irwin", "manga_pequena_mora"}

VARIETY_CORRECTIONS = {
    "chile_dulce": "chiledulce", "platano": "platano_verde", "manga_grande_cavallini": "manga", "zuquini": "zucchini"
}

CSV_FILE = "preciosCNP.csv"  
FIXTURE_FILE = "price.json"

fixture = []

with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for row in reader:
        nombre = row["NOMBRE"].strip().lower()
        variety_raw = row["variety"].strip().lower()

        if nombre in EXCLUDED_PRODUCTS or variety_raw in EXCLUDED_PRODUCTS:
            continue

        try:
            pub_date = datetime.strptime(row["publication_date"], "%Y-%m-%d").date()
            price_str = row["price"].replace(",", "").strip()
            if not price_str.isdigit():
                continue
            price = int(price_str)

            price_id = str(uuid4()) 
            
            corrected_variety = VARIETY_CORRECTIONS.get(variety_raw, variety_raw)

            fixture.append({
                "model": "products.price",
                "pk": price_id,
                "fields": {
                    "price_id": price_id,
                    "variety": corrected_variety,
                    "unit": row["unit"].strip(),
                    "price": price,
                    "publication_date": str(pub_date),
                    "year": pub_date.isocalendar()[0],
                    "week": pub_date.isocalendar()[1],
                    "quality": row["quality"].strip() or None,
                    "size": row["size"].strip() or None,
                    "sale_format": row["sale_format"].strip() or None,
                }
            })
        except Exception as e:
            print(f"Error en fila con nombre '{nombre}': {e}")
            continue

with open(FIXTURE_FILE, "w", encoding="utf-8") as f:
    json.dump(fixture, f, ensure_ascii=False, indent=4)

print(f"Fixture creado: {FIXTURE_FILE} ({len(fixture)} registros)")
