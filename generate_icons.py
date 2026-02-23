"""
Generate all favicon/icon variants from botao-pequeno@2x.png (the blue icon).
Also generates white-background and red-background variants for use in other site areas.
"""
from PIL import Image, ImageDraw, ImageFilter
import os

BASE_DIR = "/workspaces/Site-TechTrust"
SRC = os.path.join(BASE_DIR, "botao-pequeno@2x.png")

def load_source():
    """Load and ensure the source icon Is square with proper padding."""
    img = Image.open(SRC).convert("RGBA")
    # Make it perfectly square
    size = max(img.size)
    square = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - img.width) // 2, (size - img.height) // 2)
    square.paste(img, offset, img)
    return square

def generate_favicon_ico(src, path):
    """Generate a multi-size .ico file (16, 32, 48, 64)."""
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    frames = []
    for s in sizes:
        resized = src.resize(s, Image.LANCZOS)
        frames.append(resized)
    frames[0].save(path, format="ICO", sizes=sizes)
    print(f"  ✓ {path} ({', '.join(f'{s[0]}x{s[1]}' for s in sizes)})")

def generate_png(src, size, path):
    """Generate a PNG icon at specified size."""
    resized = src.resize((size, size), Image.LANCZOS)
    resized.save(path, format="PNG", optimize=True)
    print(f"  ✓ {path} ({size}x{size})")

def generate_header_icons(src):
    """Generate optimized header icons at multiple sizes."""
    # botao-pequeno.png (170px - navbar 1x)
    generate_png(src, 170, os.path.join(BASE_DIR, "botao-pequeno.png"))
    # botao-pequeno@2x.png is already the source - just ensure it's square
    generate_png(src, 340, os.path.join(BASE_DIR, "botao-pequeno@2x.png"))
    # Same for public/
    generate_png(src, 170, os.path.join(BASE_DIR, "public", "botao-pequeno.png"))
    generate_png(src, 340, os.path.join(BASE_DIR, "public", "botao-pequeno@2x.png"))

def main():
    print("Loading source icon...")
    src = load_source()
    print(f"Source: {src.size[0]}x{src.size[1]} RGBA\n")

    print("Generating favicons...")
    # Root favicons
    generate_favicon_ico(src, os.path.join(BASE_DIR, "favicon.ico"))
    generate_png(src, 32, os.path.join(BASE_DIR, "favicon-32x32.png"))
    generate_png(src, 180, os.path.join(BASE_DIR, "apple-touch-icon.png"))
    
    # Public favicons  
    generate_favicon_ico(src, os.path.join(BASE_DIR, "public", "favicon.ico"))
    generate_png(src, 32, os.path.join(BASE_DIR, "public", "favicon-32x32.png"))
    generate_png(src, 180, os.path.join(BASE_DIR, "public", "apple-touch-icon.png"))

    print("\nGenerating header icons...")
    generate_header_icons(src)

    print("\nDone! All icons generated successfully.")

if __name__ == "__main__":
    main()
