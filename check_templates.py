import csv
import os
from collections import defaultdict

# ---------- PATHS ----------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "Images/Templates")
CSV_DIR = os.path.join(SCRIPT_DIR, "csv")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "template_matching_report.txt")

# ---------- HELPER FUNCTIONS ----------
def get_available_templates():
    """Get all available template files."""
    templates = set()
    if os.path.exists(TEMPLATES_DIR):
        for filename in os.listdir(TEMPLATES_DIR):
            if filename.endswith('.png'):
                # Remove .png and replace underscore with space
                template_name = filename.replace('.png', '').replace('_', ' ')
                templates.add(template_name)
    return templates

def read_csv_countries():
    """Read all unique countries from CSV with their row numbers and cities."""
    countries = defaultdict(lambda: {'count': 0, 'rows': [], 'cities': []})
    csv_path = os.path.join(CSV_DIR, 'Countries.csv')
    
    if not os.path.exists(csv_path):
        print(f"[ERROR] CSV file not found: {csv_path}")
        return countries
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):  # Start from 2 (1 is header)
            country = row.get('Country', '').strip()
            city = row.get('City', '').strip()
            if country:
                countries[country]['count'] += 1
                countries[country]['rows'].append(row_num)
                if city:
                    countries[country]['cities'].append(city)
    
    return countries

def generate_report():
    """Generate a matching/non-matching template report."""
    templates = get_available_templates()
    csv_countries = read_csv_countries()
    
    print("[INFO] Starting template matching analysis...")
    print(f"[INFO] Found {len(templates)} template files")
    print(f"[INFO] Found {len(csv_countries)} unique countries in CSV")
    
    # Separate matching and non-matching
    matching = {}
    non_matching = {}
    
    for country in sorted(csv_countries.keys()):
        count = csv_countries[country]['count']
        rows = csv_countries[country]['rows']
        if country in templates:
            matching[country] = {'count': count, 'rows': rows}
        else:
            non_matching[country] = {'count': count, 'rows': rows}
    
    # Generate report content
    report_lines = []
    report_lines.append("=" * 100)
    report_lines.append("TEMPLATE MATCHING REPORT")
    report_lines.append("=" * 100)
    report_lines.append("")
    
    # Summary
    total_entries = sum(csv_countries[c]['count'] for c in csv_countries)
    matching_entries = sum(matching[c]['count'] for c in matching)
    non_matching_entries = sum(non_matching[c]['count'] for c in non_matching)
    
    report_lines.append("SUMMARY")
    report_lines.append("-" * 100)
    report_lines.append(f"Total CSV Entries: {total_entries}")
    report_lines.append(f"Total Unique Countries: {len(csv_countries)}")
    report_lines.append(f"Countries WITH templates: {len(matching)}")
    report_lines.append(f"Countries WITHOUT templates: {len(non_matching)}")
    report_lines.append(f"")
    report_lines.append(f"Images that CAN be generated: {matching_entries}")
    report_lines.append(f"Images that CANNOT be generated: {non_matching_entries}")
    report_lines.append("")
    report_lines.append("")
    
    # Matching countries
    report_lines.append("=" * 100)
    report_lines.append("✓ COUNTRIES WITH MATCHING TEMPLATES")
    report_lines.append("=" * 100)
    for country in sorted(matching.keys()):
        count = matching[country]['count']
        rows = matching[country]['rows']
        rows_str = f"Rows: {min(rows)}-{max(rows)}" if len(rows) > 1 else f"Row: {rows[0]}"
        report_lines.append(f"  {country:25} - {count:3} cities | {rows_str:20} | Template: {country.replace(' ', '_')}.png")
    report_lines.append("")
    report_lines.append("")
    
    # Non-matching countries (only row ranges)
    report_lines.append("=" * 100)
    report_lines.append("✗ COUNTRIES WITHOUT MATCHING TEMPLATES (NEEDS ACTION)")
    report_lines.append("=" * 100)
    for country in sorted(non_matching.keys()):
        count = non_matching[country]['count']
        rows = non_matching[country]['rows']
        rows_str = f"Rows: {min(rows)}-{max(rows)}" if len(rows) > 1 else f"Row: {rows[0]}"
        report_lines.append(f"  {country:25} - {count:3} cities | {rows_str:20} | MISSING: {country.replace(' ', '_')}.png")
    report_lines.append("")
    report_lines.append("")
    
    # Available templates not in CSV
    report_lines.append("=" * 100)
    report_lines.append("TEMPLATES AVAILABLE BUT NOT IN CSV (EXTRA TEMPLATES)")
    report_lines.append("=" * 100)
    extra_templates = templates - set(csv_countries.keys())
    if extra_templates:
        for template in sorted(extra_templates):
            report_lines.append(f"  {template.replace('_', ' ')}.png")
    else:
        report_lines.append("  None")
    report_lines.append("")
    report_lines.append("")
    
    # Write to file
    report_content = "\n".join(report_lines)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"[OK] Report generated: {OUTPUT_FILE}")
    print("")
    print(report_content)
    
    return {
        'total_entries': total_entries,
        'matching': matching,
        'non_matching': non_matching,
        'extra_templates': extra_templates
    }

if __name__ == "__main__":
    generate_report()
