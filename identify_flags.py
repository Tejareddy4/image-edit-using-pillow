from PIL import Image
import os
import numpy as np
from collections import Counter

# Get the flags directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FLAGS_DIR = os.path.join(SCRIPT_DIR, "Images/flags")

# Common flag color patterns (dominant colors) for identification
# This is a simplified approach - in practice, you'd need more sophisticated recognition
FLAG_PATTERNS = {
    "India": {
        "colors": ["#FF9933", "#FFFFFF", "#138808"],  # Saffron, White, Green
        "pattern": "horizontal_stripes"
    },
    "United_States": {
        "colors": ["#B22234", "#FFFFFF", "#3C3B6E"],  # Red, White, Blue
        "pattern": "stars_and_stripes"
    },
    "United_Kingdom": {
        "colors": ["#012169", "#FFFFFF", "#C8102E"],  # Blue, White, Red
        "pattern": "union_jack"
    },
    "United_Arab_Emirates": {
        "colors": ["#FF0000", "#000000", "#FFFFFF", "#007A3D"],  # Red, Black, White, Green
        "pattern": "vertical_stripes"
    },
    "Austria": {
        "colors": ["#ED2939", "#FFFFFF"],  # Red, White
        "pattern": "horizontal_stripes"
    },
    "Belgium": {
        "colors": ["#000000", "#FAE042", "#ED2939"],  # Black, Yellow, Red
        "pattern": "vertical_stripes"
    },
    "Bulgaria": {
        "colors": ["#FFFFFF", "#00966E", "#D62612"],  # White, Green, Red
        "pattern": "horizontal_stripes"
    },
    "Canada": {
        "colors": ["#FF0000", "#FFFFFF"],  # Red, White
        "pattern": "maple_leaf"
    },
    "Croatia": {
        "colors": ["#FF0000", "#FFFFFF", "#171796"],  # Red, White, Blue
        "pattern": "checkerboard"
    },
    "Czech_Republic": {
        "colors": ["#FFFFFF", "#D7141A", "#11457E"],  # White, Red, Blue
        "pattern": "horizontal_stripes_triangle"
    },
    "European_Union": {
        "colors": ["#003399", "#FFCC00"],  # Blue, Yellow
        "pattern": "stars_circle"
    },
    "France": {
        "colors": ["#0055A4", "#FFFFFF", "#EF4135"],  # Blue, White, Red
        "pattern": "vertical_stripes"
    },
    "Germany": {
        "colors": ["#000000", "#DD0000", "#FFCE00"],  # Black, Red, Yellow
        "pattern": "horizontal_stripes"
    },
    "Italy": {
        "colors": ["#009246", "#FFFFFF", "#CE2B37"],  # Green, White, Red
        "pattern": "vertical_stripes"
    },
    "Portugal": {
        "colors": ["#006600", "#FF0000"],  # Green, Red
        "pattern": "vertical_split"
    }
}

def rgb_to_hex(r, g, b):
    """Convert RGB to hex color."""
    return f"#{r:02X}{g:02X}{b:02X}"

def get_dominant_colors(image, num_colors=5):
    """Get dominant colors from an image."""
    # Resize for faster processing
    image = image.resize((150, 100), Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    
    # Count color frequencies
    color_counts = Counter(pixels)
    top_colors = color_counts.most_common(num_colors)
    
    # Convert to hex
    hex_colors = []
    for color, count in top_colors:
        if len(color) == 4:  # RGBA
            r, g, b, a = color
        elif len(color) == 3:  # RGB
            r, g, b = color
        else:
            continue
        hex_colors.append(rgb_to_hex(r, g, b))
    
    return hex_colors

def color_distance(hex1, hex2):
    """Calculate color distance between two hex colors."""
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    return sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)) ** 0.5

def identify_flag(image_path):
    """Try to identify a flag based on its colors."""
    try:
        img = Image.open(image_path).convert("RGB")
        dominant_colors = get_dominant_colors(img)
        
        best_match = None
        best_score = float('inf')
        
        for country, pattern_info in FLAG_PATTERNS.items():
            expected_colors = pattern_info["colors"]
            score = 0
            
            # Check how many expected colors match
            matches = 0
            for exp_color in expected_colors:
                for dom_color in dominant_colors:
                    distance = color_distance(exp_color, dom_color)
                    if distance < 50:  # Threshold for color matching
                        matches += 1
                        break
            
            # Calculate score (lower is better)
            score = len(expected_colors) - matches
            
            if score < best_score:
                best_score = score
                best_match = country
        
        return best_match
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def rename_flags():
    """Identify and rename flag images."""
    if not os.path.exists(FLAGS_DIR):
        print(f"Flags directory not found: {FLAGS_DIR}")
        return
    
    flag_files = [f for f in os.listdir(FLAGS_DIR) if f.lower().endswith('.png')]
    flag_files.sort()
    
    print(f"Found {len(flag_files)} flag files to identify...")
    print("-" * 60)
    
    renamed_count = 0
    for flag_file in flag_files:
        old_path = os.path.join(FLAGS_DIR, flag_file)
        print(f"\nAnalyzing: {flag_file}")
        
        country = identify_flag(old_path)
        
        if country:
            new_name = f"{country}.png"
            new_path = os.path.join(FLAGS_DIR, new_name)
            
            # Check if target file already exists
            if os.path.exists(new_path) and old_path != new_path:
                # Add a number suffix
                base_name = country
                counter = 1
                while os.path.exists(new_path):
                    new_name = f"{base_name}_{counter}.png"
                    new_path = os.path.join(FLAGS_DIR, new_name)
                    counter += 1
            
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"  [OK] Renamed to: {new_name}")
                renamed_count += 1
            else:
                print(f"  [-] Already correctly named")
        else:
            print(f"  [X] Could not identify flag")
    
    print("\n" + "-" * 60)
    print(f"Renamed {renamed_count} files")

if __name__ == "__main__":
    rename_flags()

