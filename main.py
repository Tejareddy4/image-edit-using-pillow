from PIL import Image, ImageDraw, ImageFont
import os
import random

# ---------- INPUT ----------
CITY = "Bawana Industrial Area"
ORIGIN_COUNTRY = "India"  # Origin country (left side flag)
COUNTRY = "Belgium"  # Destination country (right side flag)

# ---------- FILES ----------
# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(SCRIPT_DIR, "Images/template.png")
FONT_PATH = os.path.join(SCRIPT_DIR, "fonts/Poppins-Bold.ttf")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
# FLAGS_DIR = os.path.join(SCRIPT_DIR, "images/flags")
COUNTRIES_DIR = os.path.join(SCRIPT_DIR, "Images/countries")

# ---------- COUNTRY TO FLAG MAPPING ----------
# COUNTRY_TO_FLAG = {
#     "India": "India",
#     "IN": "India",
#     "US": "United_States",
#     "USA": "United_States",
#     "United States": "United_States",
#     "UK": "United_Kingdom",
#     "United Kingdom": "United_Kingdom",
#     "UAE": "United_Arab_Emirates",
#     "United Arab Emirates": "United_Arab_Emirates",
#     "Austria": "Austria",
#     "Belgium": "Belgium",
#     "Bulgaria": "Bulgaria",
#     "Canada": "Canada",
#     "Croatia": "Croatia",
#     "Czech Republic": "Czech_Republic",
#     "Czech": "Czech_Republic",
#     "EU": "European_Union",
#     "European Union": "European_Union",
#     "Europe": "European_Union",
#     "France": "France",
#     "Germany": "Germany",
#     "Italy": "Italy",
#     "Portugal": "Portugal",
# }

# ---------- HELPER FUNCTIONS ----------
def wrap_text(text, max_chars=22):
    """Wrap text into multiple lines, ensuring no line exceeds max_chars characters."""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        # Check if adding this word would exceed the limit
        test_line = current_line + (" " if current_line else "") + word
        if len(test_line) <= max_chars:
            current_line = test_line
        else:
            # If current_line is not empty, save it and start a new line
            if current_line:
                lines.append(current_line)
            current_line = word
            # If a single word exceeds the limit, add it anyway (could be split further if needed)
            if len(word) > max_chars:
                # Split long word (though this shouldn't happen in practice)
                lines.append(word[:max_chars])
                current_line = word[max_chars:]
    
    # Add the last line
    if current_line:
        lines.append(current_line)
    
    return lines if lines else [text]

# def get_flag_path(country):
#     """Get the flag image path for a given country."""
#     flag_name = COUNTRY_TO_FLAG.get(country, country.replace(" ", "_"))
#     flag_path = os.path.join(FLAGS_DIR, f"{flag_name}.png")
#     if os.path.exists(flag_path):
#         return flag_path
#     return None

def get_country_images(country_name):
    """Get all country images for a given country.
    Handles both single PNG files (e.g., Belgium.png) and multiple numbered files (e.g., india1.png, india2.png).
    """
    country_images = []
    country_lower = country_name.lower()
    country_title = country_name.title()
    
    # Check for single PNG file directly in countries directory (e.g., Belgium.png)
    single_file_title = os.path.join(COUNTRIES_DIR, f"{country_title}.png")
    single_file_lower = os.path.join(COUNTRIES_DIR, f"{country_lower}.png")
    
    if os.path.exists(single_file_title):
        country_images.append(single_file_title)
    elif os.path.exists(single_file_lower):
        country_images.append(single_file_lower)
    
    # Check for numbered files (e.g., india1.png, india2.png, indian2.png)
    if os.path.exists(COUNTRIES_DIR):
        for filename in os.listdir(COUNTRIES_DIR):
            if filename.lower().startswith(country_lower) and filename.endswith('.png'):
                # Skip if already added as single file
                file_path = os.path.join(COUNTRIES_DIR, filename)
                if file_path not in country_images:
                    country_images.append(file_path)
    
    return sorted(country_images)

# ---------- LOAD ----------
base = Image.open(TEMPLATE).convert("RGBA")
draw = ImageDraw.Draw(base)
base_width, base_height = base.size

# Load origin flag (left side) - COMMENTED OUT
# origin_flag_path = get_flag_path(ORIGIN_COUNTRY)
# if origin_flag_path:
#     origin_flag = Image.open(origin_flag_path).convert("RGBA")
#     # Resize flag to appropriate size (adjust as needed)
#     flag_width = 120
#     flag_height = int(origin_flag.height * (flag_width / origin_flag.width))
#     origin_flag = origin_flag.resize((flag_width, flag_height), Image.Resampling.LANCZOS)
#     # Position: left side, below the box area (adjust coordinates as needed)
#     origin_flag_x = 150
#     origin_flag_y = base_height - 200
#     base.paste(origin_flag, (origin_flag_x, origin_flag_y), origin_flag)
#     print(f"[OK] Loaded origin flag: {origin_flag_path}")
# else:
#     print(f"[WARNING] Origin flag not found for: {ORIGIN_COUNTRY}")

# Load destination flag (right side) - COMMENTED OUT
# dest_flag_path = get_flag_path(COUNTRY)
# if dest_flag_path:
#     dest_flag = Image.open(dest_flag_path).convert("RGBA")
#     # Resize flag to appropriate size
#     flag_width = 120
#     flag_height = int(dest_flag.height * (flag_width / dest_flag.width))
#     dest_flag = dest_flag.resize((flag_width, flag_height), Image.Resampling.LANCZOS)
#     # Position: right side, near Statue of Liberty (adjust coordinates as needed)
#     dest_flag_x = base_width - 250
#     dest_flag_y = base_height - 200
#     base.paste(dest_flag, (dest_flag_x, dest_flag_y), dest_flag)
#     print(f"[OK] Loaded destination flag: {dest_flag_path}")
# else:
#     print(f"[WARNING] Destination flag not found for: {COUNTRY}")

# Load and paste origin country images (left side) - COMMENTED OUT
# origin_country_images = get_country_images(ORIGIN_COUNTRY)
# if origin_country_images:
#     print(f"[OK] Found {len(origin_country_images)} origin country images for {ORIGIN_COUNTRY}")
#     # Randomly select one image from available images
#     selected_image = random.choice(origin_country_images)
#     try:
#         country_img = Image.open(selected_image).convert("RGBA")
#         # Resize country image to appropriate size (adjust as needed)
#         img_width = 300
#         img_height = int(country_img.height * (img_width / country_img.width))
#         country_img = country_img.resize((img_width, img_height), Image.Resampling.LANCZOS)
#         # Position on left side (adjust coordinates as needed)
#         img_x = 100
#         img_y = base_height - img_height - 150
#         base.paste(country_img, (img_x, img_y), country_img)
#         print(f"[OK] Pasted origin country image: {selected_image}")
#     except Exception as e:
#         print(f"[WARNING] Error loading origin country image {selected_image}: {e}")
# else:
#     print(f"[WARNING] No origin country images found for: {ORIGIN_COUNTRY}")

# Load and paste destination country images (right side) - COMMENTED OUT
# dest_country_images = get_country_images(COUNTRY)
# if dest_country_images:
#     print(f"[OK] Found {len(dest_country_images)} destination country images for {COUNTRY}")
#     # Randomly select one image from available images
#     selected_image = random.choice(dest_country_images)
#     try:
#         country_img = Image.open(selected_image).convert("RGBA")
#         # Resize country image to appropriate size
#         img_width = 300
#         img_height = int(country_img.height * (img_width / country_img.width))
#         country_img = country_img.resize((img_width, img_height), Image.Resampling.LANCZOS)
#         # Position on right side (adjust coordinates as needed)
#         img_x = base_width - img_width - 100
#         img_y = base_height - img_height - 150
#         base.paste(country_img, (img_x, img_y), country_img)
#         print(f"[OK] Pasted destination country image: {selected_image}")
#     except Exception as e:
#         print(f"[WARNING] Error loading destination country image {selected_image}: {e}")
# else:
#     print(f"[WARNING] No destination country images found for: {COUNTRY}")

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
x = 298   # ← start after "from"// width (first line)
y = 213  #height position (first line)
x_next = 146  # x position for wrapped lines
y_next = 280  # y position for wrapped lines

text = f"{CITY} to {COUNTRY}"

# Wrap text if it exceeds 22 characters per line
text_lines = wrap_text(text, max_chars=22)

# Draw first line at original position, subsequent lines at (136, 341) and below
if text_lines:
    # Draw first line at original position
    draw.text(
        (x, y),
        text_lines[0],
        fill="#1677ff",
        font=font
    )
    
    # Draw remaining lines starting from (146, 305)
    if len(text_lines) > 1:
        # Calculate line height for spacing between wrapped lines
        try:
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), text_lines[1], font=font)
                line_height = bbox[3] - bbox[1] + 10  # Add 10px spacing between lines
            else:
                line_height = font.getsize(text_lines[1])[1] + 10
        except:
            # Fallback: estimate based on font size (approximately font_size * 1.2 + spacing)
            line_height = 80  # Approximate for 64pt font
        
        # Draw remaining lines
        for i, line in enumerate(text_lines[1:], start=1):
            draw.text(
                (x_next, y_next + (i - 1) * line_height),
                line,
                fill="#1677ff",
                font=font
            )

# ---------- SAVE ----------
os.makedirs(OUTPUT_DIR, exist_ok=True)
out = f"{OUTPUT_DIR}/{CITY.lower().replace(' ','-')}-to-{COUNTRY.lower()}.png"
base.save(out)

print("[OK] Generated:", out)
