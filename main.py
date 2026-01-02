from PIL import Image, ImageDraw, ImageFont
import os
import csv

# ---------- FILES ----------
# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- INPUT ----------
ORIGIN_COUNTRY = "India"  # Origin country (left side flag)
CSV_FILE = os.path.join(SCRIPT_DIR, "csv/country and city.csv")
TEMPLATE = os.path.join(SCRIPT_DIR, "Images/template.png")
FONT_PATH = os.path.join(SCRIPT_DIR, "fonts/Poppins-Bold.ttf")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
FLAGS_DIR = os.path.join(SCRIPT_DIR, "Images/flags")
COUNTRIES_DIR = os.path.join(SCRIPT_DIR, "Images/countries")

# ---------- COUNTRY TO FLAG MAPPING ----------
COUNTRY_TO_FLAG = {
    "India": "India",
    "IN": "India",
    "US": "United_States",
    "USA": "United_States",
    "United States": "United_States",
    "UK": "United_Kingdom",
    "United Kingdom": "United_Kingdom",
    "UAE": "United_Arab_Emirates",
    "United Arab Emirates": "United_Arab_Emirates",
    "Austria": "Austria",
    "Belgium": "Belgium",
    "Bulgaria": "Bulgaria",
    "Canada": "Canada",
    "Croatia": "Croatia",
    "Czech Republic": "Czech_Republic",
    "Czech": "Czech_Republic",
    "EU": "European_Union",
    "European Union": "European_Union",
    "Europe": "European_Union",
    "France": "France",
    "Germany": "Germany",
    "Italy": "Italy",
    "Portugal": "Portugal",
}

# ---------- HELPER FUNCTIONS ----------
def get_flag_path(country):
    """Get the flag image path for a given country."""
    flag_name = COUNTRY_TO_FLAG.get(country, country.replace(" ", "_"))
    flag_path = os.path.join(FLAGS_DIR, f"{flag_name}.png")
    if os.path.exists(flag_path):
        return flag_path
    return None

def get_country_images(country_name):
    """Get all country images for a given country (e.g., india1.png, india2.png, etc.)."""
    country_dir = os.path.join(COUNTRIES_DIR, country_name.lower())
    if os.path.exists(country_dir):
        images = sorted([f for f in os.listdir(country_dir) if f.endswith('.png')])
        return [os.path.join(country_dir, img) for img in images]
    return []

def generate_image(city, country):
    """Generate an image for a given city and country."""
    # Load template
    base = Image.open(TEMPLATE).convert("RGBA")
    draw = ImageDraw.Draw(base)
    base_width, base_height = base.size
    
    # Load origin flag (left side)
    origin_flag_path = get_flag_path(ORIGIN_COUNTRY)
    if origin_flag_path:
        origin_flag = Image.open(origin_flag_path).convert("RGBA")
        flag_width = 120
        flag_height = int(origin_flag.height * (flag_width / origin_flag.width))
        origin_flag = origin_flag.resize((flag_width, flag_height), Image.Resampling.LANCZOS)
        origin_flag_x = 150
        origin_flag_y = base_height - 200
        base.paste(origin_flag, (origin_flag_x, origin_flag_y), origin_flag)
    
    # Load destination flag (right side)
    dest_flag_path = get_flag_path(country)
    if dest_flag_path:
        dest_flag = Image.open(dest_flag_path).convert("RGBA")
        flag_width = 120
        flag_height = int(dest_flag.height * (flag_width / dest_flag.width))
        dest_flag = dest_flag.resize((flag_width, flag_height), Image.Resampling.LANCZOS)
        dest_flag_x = base_width - 250
        dest_flag_y = base_height - 200
        base.paste(dest_flag, (dest_flag_x, dest_flag_y), dest_flag)
    
    # Load font
    try:
        if os.path.exists(FONT_PATH):
            font = ImageFont.truetype(FONT_PATH, 64)
        else:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Draw text
    x = 298
    y = 213
    text = f"{city} to {country}"
    
    draw.text(
        (x, y),
        text,
        fill="#1677ff",
        font=font
    )
    
    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = f"{OUTPUT_DIR}/{city.lower().replace(' ','-')}-to-{country.lower().replace(' ','-')}.png"
    base.save(out)
    
    return out

# ---------- READ CSV AND GENERATE IMAGES ----------
if not os.path.exists(CSV_FILE):
    print(f"[ERROR] CSV file not found: {CSV_FILE}")
    exit(1)

print(f"[OK] Reading CSV file: {CSV_FILE}")
generated_count = 0
skipped_count = 0

with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        country = row.get('Country', '').strip()
        city = row.get('City', '').strip()
        
        # Skip rows with empty city or country
        if not city or not country:
            skipped_count += 1
            continue
        
        try:
            output_path = generate_image(city, country)
            generated_count += 1
            if generated_count % 10 == 0:
                print(f"[PROGRESS] Generated {generated_count} images...")
        except Exception as e:
            print(f"[ERROR] Failed to generate image for {city} to {country}: {e}")
            skipped_count += 1

print(f"\n[OK] Completed!")
print(f"    Generated: {generated_count} images")
print(f"    Skipped: {skipped_count} rows")
