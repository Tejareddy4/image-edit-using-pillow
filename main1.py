from PIL import Image, ImageDraw, ImageFont
import os
import random
import csv

# ---------- FILES ----------
# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "Images/Templates")
FONT_PATH = os.path.join(SCRIPT_DIR, "fonts/Poppins-Bold.ttf")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
CSV_DIR = os.path.join(SCRIPT_DIR, "csv")
COUNTRIES_DIR = os.path.join(SCRIPT_DIR, "Images/countries")

# Origin country for all shipments (can be changed)
ORIGIN_COUNTRY = "India"

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

def get_template_path(country_name):
    """Get the template image path for a given country.
    Tries multiple naming formats: Title_Case, lowercase, and original.
    """
    # Try different formats
    country_title = country_name.replace(" ", "_").title()
    country_lower = country_name.replace(" ", "_").lower()
    country_original = country_name.replace(" ", "_")
    
    # Check for template files in different formats
    template_options = [
        os.path.join(TEMPLATES_DIR, f"{country_title}.png"),
        os.path.join(TEMPLATES_DIR, f"{country_original}.png"),
        os.path.join(TEMPLATES_DIR, f"{country_lower}.png"),
        os.path.join(TEMPLATES_DIR, f"{country_name}.png"),
    ]
    
    for template_path in template_options:
        if os.path.exists(template_path):
            return template_path
    
    # If no template found, return None
    return None

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

def get_csv_file():
    """Get the first CSV file in the csv directory."""
    if os.path.exists(CSV_DIR):
        for filename in os.listdir(CSV_DIR):
            if filename.endswith('.csv'):
                return os.path.join(CSV_DIR, filename)
    return None

def process_image(city, country):
    """Process a single image generation for the given city and country."""
    
    # Skip if country is empty
    if not country or country.strip() == "":
        print(f"[SKIP] {city} - No country specified")
        return False
    
    print(f"\n[PROCESSING] {city} to {country}")
    
    # ---------- LOAD TEMPLATE ----------
    # Get template based on destination country
    template_path = get_template_path(country)
    if not template_path:
        print(f"[SKIP] Template not found for country: {country}")
        return False
    
    try:
        base = Image.open(template_path).convert("RGBA")
        print(f"[OK] Loaded template: {template_path}")
    except Exception as e:
        print(f"[ERROR] Failed to load template: {e}")
        return False
    
    draw = ImageDraw.Draw(base)
    base_width, base_height = base.size
    
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
    # dest_country_images = get_country_images(country)
    # if dest_country_images:
    #     print(f"[OK] Found {len(dest_country_images)} destination country images for {country}")
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
    #     print(f"[WARNING] No destination country images found for: {country}")
    
    # ---------- FONT ----------
    try:
        if os.path.exists(FONT_PATH):
            font = ImageFont.truetype(FONT_PATH, 64)
        else:
            print(f"[WARNING] Font file not found, using default font")
            font = ImageFont.load_default()
    except Exception as e:
        print(f"[WARNING] Error loading font: {e}")
        font = ImageFont.load_default()
    
    # ---------- POSITION ----------
    # Adjust these to align exactly after "from" in your template
    x = 298   # ← start after "from"// width (first line)
    y = 213  #height position (first line)
    x_next = 146  # x position for wrapped lines
    y_next = 280  # y position for wrapped lines
    
    text = f"{city} to {country}"
    
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
    # Create country-specific output directory
    country_output_dir = os.path.join(OUTPUT_DIR, country.replace(" ", "_"))
    os.makedirs(country_output_dir, exist_ok=True)
    
    # Save output in country folder
    out = os.path.join(country_output_dir, f"{city.lower().replace(' ','-')}-to-{country.lower().replace(' ', '-')}.png")
    base.save(out)
    
    print(f"[OK] Generated: {out}")
    return True

# ---------- MAIN ----------
def main():
    # Get CSV file
    csv_file = get_csv_file()
    if not csv_file:
        print("[ERROR] No CSV file found in csv directory")
        return
    
    print(f"[OK] Reading CSV file: {csv_file}")
    
    # Read CSV and process each row
    processed = 0
    skipped = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Get country and city from the row
                # Assuming columns: "Country" and "City"
                country = row.get('Country', '').strip()
                city = row.get('City', '').strip()
                
                if city and country:
                    if process_image(city, country):
                        processed += 1
                    else:
                        skipped += 1
                else:
                    skipped += 1
    
    except Exception as e:
        print(f"[ERROR] Failed to read CSV file: {e}")
        return
    
    print(f"\n{'='*50}")
    print(f"[SUMMARY] Processed: {processed} | Skipped: {skipped}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
