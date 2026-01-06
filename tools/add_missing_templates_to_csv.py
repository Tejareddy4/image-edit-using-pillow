import csv
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'csv', 'Countries.csv')
CSV_PATH = os.path.normpath(CSV_PATH)

MISSING_COUNTRIES = [
    'Denmark', 'Estonia', 'Finland', 'Greece'
]

def read_rows(path):
    with open(path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = list(reader)
    return header, rows


def write_rows(path, header, rows):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def get_city_list(rows, source_country):
    # Preserve order of appearance for the source country
    cities = []
    for r in rows:
        if r.get('Country', '').strip() == source_country:
            city = (r.get('City') or '').strip()
            if city and city not in cities:
                cities.append(city)
    return cities


def next_s_no(rows):
    max_no = 0
    for r in rows:
        try:
            max_no = max(max_no, int((r.get('S_no') or '0').strip()))
        except ValueError:
            continue
    return max_no + 1


def main():
    if not os.path.exists(CSV_PATH):
        raise SystemExit(f"CSV not found: {CSV_PATH}")

    header, rows = read_rows(CSV_PATH)
    required_cols = ['S_no', 'Country', 'City', 'City to country name']
    if header != required_cols:
        # Try to align header order if possible
        header = required_cols

    # Cities to replicate: use the first fully-populated block, prefer 'Belgium' then 'US'
    cities = get_city_list(rows, 'Belgium')
    if len(cities) == 0:
        cities = get_city_list(rows, 'US')
    if len(cities) == 0:
        raise SystemExit('Could not derive city list from CSV (Belgium/US)')

    # Build a set of existing countries
    existing_countries = set(r.get('Country', '').strip() for r in rows if r.get('Country'))

    to_add = [c for c in MISSING_COUNTRIES if c not in existing_countries]
    if not to_add:
        print('No missing countries to add. CSV already contains all target countries.')
        return

    s_no = next_s_no(rows)
    added = 0
    for country in to_add:
        for city in cities:
            rows.append({
                'S_no': str(s_no),
                'Country': country,
                'City': city,
                'City to country name': f"{city} to {country}"
            })
            s_no += 1
            added += 1

    write_rows(CSV_PATH, header, rows)
    print(f"Added {added} rows for countries: {to_add}")

if __name__ == '__main__':
    main()
