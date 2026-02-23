"""
Generate white-background and red-background icon variants
from the blue icon for use in different site sections.
"""
from PIL import Image, ImageDraw, ImageEnhance
import os

BASE_DIR = "/workspaces/Site-TechTrust"
SRC = os.path.join(BASE_DIR, "botao-pequeno@2x.png")

def load_source():
    img = Image.open(SRC).convert("RGBA")
    size = max(img.size)
    square = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - img.width) // 2, (size - img.height) // 2)
    square.paste(img, offset, img)
    return square

def create_white_variant(src, size=340):
    """Create icon with white/light background - dark blue logo on white."""
    src_resized = src.resize((size, size), Image.LANCZOS)
    
    # Create white rounded-rect background
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)
    radius = size // 5
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=(245, 247, 250, 255))
    
    # Extract the icon shape (non-transparent pixels)
    # Place the original on white bg but darken it slightly for contrast
    icon = src_resized.copy()
    
    # Paste icon centered on white background
    bg.paste(icon, (0, 0), icon)
    
    return bg

def create_red_variant(src, size=340):
    """Create icon with red background - blue logo on red."""
    src_resized = src.resize((size, size), Image.LANCZOS)
    
    # Create red rounded-rect background
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)
    radius = size // 5
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=(204, 34, 51, 255))
    
    # Paste the blue icon on red background
    bg.paste(src_resized, (0, 0), src_resized)
    
    return bg

def main():
    print("Loading source icon...")
    src = load_source()
    
    print("Generating white variant...")
    white = create_white_variant(src)
    white_path = os.path.join(BASE_DIR, "icon-white.png")
    white.save(white_path, format="PNG", optimize=True)
    print(f"  ✓ {white_path}")
    
    # Also save small version
    white_sm = white.resize((170, 170), Image.LANCZOS)
    white_sm_path = os.path.join(BASE_DIR, "icon-white-sm.png")
    white_sm.save(white_sm_path, format="PNG", optimize=True)
    print(f"  ✓ {white_sm_path}")
    
    print("Generating red variant...")
    red = create_red_variant(src)
    red_path = os.path.join(BASE_DIR, "icon-red.png")
    red.save(red_path, format="PNG", optimize=True)
    print(f"  ✓ {red_path}")
    
    red_sm = red.resize((170, 170), Image.LANCZOS)
    red_sm_path = os.path.join(BASE_DIR, "icon-red-sm.png")
    red_sm.save(red_sm_path, format="PNG", optimize=True)
    print(f"  ✓ {red_sm_path}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
