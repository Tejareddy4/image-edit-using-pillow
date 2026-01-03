from PIL import Image, ImageDraw, ImageFont
import os

# ---------- INPUT ----------
CITY = "Bawana Industrial Area"
ORIGIN_COUNTRY = "India"  # Origin country (left side flag)
COUNTRY = "US"  # Destination country (right side flag)

# ---------- FILES ----------
# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
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

# ---------- LOAD ----------
base = Image.open(TEMPLATE).convert("RGBA")
draw = ImageDraw.Draw(base)
base_width, base_height = base.size

# Load origin flag (left side)
origin_flag_path = get_flag_path(ORIGIN_COUNTRY)
if origin_flag_path:
    origin_flag = Image.open(origin_flag_path).convert("RGBA")
    # Resize flag to appropriate size (adjust as needed)
    flag_width = 120
    flag_height = int(origin_flag.height * (flag_width / origin_flag.width))
    origin_flag = origin_flag.resize((flag_width, flag_height), Image.Resampling.LANCZOS)
    # Position: left side, below the box area (adjust coordinates as needed)
    origin_flag_x = 150
    origin_flag_y = base_height - 200
    base.paste(origin_flag, (origin_flag_x, origin_flag_y), origin_flag)
    print(f"[OK] Loaded origin flag: {origin_flag_path}")
else:
    print(f"[WARNING] Origin flag not found for: {ORIGIN_COUNTRY}")

# Load destination flag (right side)
dest_flag_path = get_flag_path(COUNTRY)
if dest_flag_path:
    dest_flag = Image.open(dest_flag_path).convert("RGBA")
    # Resize flag to appropriate size
    flag_width = 120
    flag_height = int(dest_flag.height * (flag_width / dest_flag.width))
    dest_flag = dest_flag.resize((flag_width, flag_height), Image.Resampling.LANCZOS)
    # Position: right side, near Statue of Liberty (adjust coordinates as needed)
    dest_flag_x = base_width - 250
    dest_flag_y = base_height - 200
    base.paste(dest_flag, (dest_flag_x, dest_flag_y), dest_flag)
    print(f"[OK] Loaded destination flag: {dest_flag_path}")
else:
    print(f"[WARNING] Destination flag not found for: {COUNTRY}")

# Load country images if available
country_images = get_country_images(COUNTRY)
if country_images:
    print(f"[OK] Found {len(country_images)} country images for {COUNTRY}")

# ---------- FONT ----------
try:
    if os.path.exists(FONT_PATH):
        font = ImageFont.truetype(FONT_PATH, 64)
        print(f"[OK] Loaded font: {FONT_PATH}")
    else:
        print(f"[WARNING] Font file not found: {FONT_PATH}")
        print(f"         Using default font instead")
        font = ImageFont.load_default()
except Exception as e:
    print(f"[WARNING] Error loading font: {e}")
    print(f"         Using default font instead")
    font = ImageFont.load_default()

# ---------- POSITION ----------
# Adjust these to align exactly after "from" in your template
x = 298   # ← start after "from"// width
y = 213  #height position

text = f"{CITY} to {COUNTRY}"

draw.text(
    (x, y),
    text,
    fill="#1677ff",
    font=font
)

# ---------- SAVE ----------
os.makedirs(OUTPUT_DIR, exist_ok=True)
out = f"{OUTPUT_DIR}/{CITY.lower().replace(' ','-')}-to-{COUNTRY.lower()}.png"
base.save(out)

print("[OK] Generated:", out)
