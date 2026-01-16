import json
import urllib.request

# https://restcountries.com/#endpoints-latest-added-enpoint documentazione di proggeto
# https://www.npmjs.com/package/@yusifaliyevpro/countries#available-fields Per vedere quali sono i campi disponibili 

URL = "https://restcountries.com/v3.1/all?fields=name,cca2,cca3,ccn3,translations"

req = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0 (compatible; MyTutorSeeder/1.0)"
    }
)

with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode("utf-8"))

rows = []
for c in data:
    name = (
        c.get("translations", {}).get("ita", {}).get("common")
        or c.get("name", {}).get("common")
    )
    iso2 = c.get("cca2")
    iso3 = c.get("cca3")
    num = c.get("ccn3")

    if not (name and iso2):
        continue

    name_sql = name.replace("'", "''")
    iso2_sql = iso2.replace("'", "''")
    iso3_sql = (iso3 or "").replace("'", "''")
    num_sql = (num or "").replace("'", "''")

    rows.append((name_sql, iso2_sql, iso3_sql if iso3 else None, num_sql if num else None))

rows.sort(key=lambda x: x[0])

with open("paesi.sql", "w", encoding="utf-8") as f:
    f.write("INSERT INTO paese (nome, iso2, iso3, iso_numeric) VALUES\n")
    values = []
    for name, iso2, iso3, num in rows:
        v = (
            f"('{name}','{iso2}',"
            + (f"'{iso3}'" if iso3 else "NULL")
            + ","
            + (f"'{num}'" if num else "NULL")
            + ")"
        )
        values.append(v)
    f.write(",\n".join(values))
    f.write(";\n")

print(f"Generati {len(rows)} paesi in paesi.sql")
