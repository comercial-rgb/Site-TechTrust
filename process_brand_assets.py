"""
Generate all favicons, header icons, and optimized images from the NEW brand assets.
Uses logo-icon-blue.png as the primary icon for favicon and header.
"""
from PIL import Image
import os

BASE = "/workspaces/Site-TechTrust"

def make_square(img):
    """Make image perfectly square with transparent padding."""
    size = max(img.size)
    square = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - img.width) // 2, (size - img.height) // 2)
    square.paste(img, offset, img)
    return square

def save_png(img, size, path):
    resized = img.resize((size, size), Image.LANCZOS)
    resized.save(path, format="PNG", optimize=True)
    print(f"  ✓ {os.path.basename(path)} ({size}x{size})")

def save_ico(img, path):
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    frames = [img.resize(s, Image.LANCZOS) for s in sizes]
    frames[0].save(path, format="ICO", sizes=sizes)
    print(f"  ✓ {os.path.basename(path)} (multi-size ICO)")

def process_icon(src_name, out_prefix):
    """Process an icon image into all needed sizes."""
    src = Image.open(os.path.join(BASE, src_name)).convert("RGBA")
    sq = make_square(src)
    
    # Header icons
    save_png(sq, 170, os.path.join(BASE, f"{out_prefix}.png"))
    save_png(sq, 340, os.path.join(BASE, f"{out_prefix}@2x.png"))
    
    # Copy to public/
    save_png(sq, 170, os.path.join(BASE, "public", f"{out_prefix}.png"))
    save_png(sq, 340, os.path.join(BASE, "public", f"{out_prefix}@2x.png"))
    
    return sq

def main():
    print("=== Processing BLUE icon (favicon + header) ===")
    blue = process_icon("logo-icon-blue.png", "botao-pequeno")
    
    # Generate favicons from blue icon
    print("\n  Favicons:")
    save_ico(blue, os.path.join(BASE, "favicon.ico"))
    save_png(blue, 32, os.path.join(BASE, "favicon-32x32.png"))
    save_png(blue, 180, os.path.join(BASE, "apple-touch-icon.png"))
    save_ico(blue, os.path.join(BASE, "public", "favicon.ico"))
    save_png(blue, 32, os.path.join(BASE, "public", "favicon-32x32.png"))
    save_png(blue, 180, os.path.join(BASE, "public", "apple-touch-icon.png"))
    
    print("\n=== Processing WHITE icon ===")
    white = process_icon("logo-icon-white.png", "icon-white")
    # Also save small version for inline use
    save_png(white, 64, os.path.join(BASE, "icon-white-sm.png"))
    
    print("\n=== Processing RED icon ===")
    red = process_icon("logo-icon-red.png", "icon-red")
    save_png(red, 64, os.path.join(BASE, "icon-red-sm.png"))
    
    print("\n=== Processing RED ALT icon ===")
    red_alt = process_icon("logo-icon-red-alt.png", "icon-red-alt")
    
    print("\n=== Processing HORIZONTAL logo ===")
    logo_h = Image.open(os.path.join(BASE, "logo-horizontal.png")).convert("RGBA")
    # Save at good web sizes
    for w in [400, 300, 200]:
        ratio = w / logo_h.width
        h = int(logo_h.height * ratio)
        resized = logo_h.resize((w, h), Image.LANCZOS)
        path = os.path.join(BASE, f"logo-horizontal-{w}w.png")
        resized.save(path, format="PNG", optimize=True)
        print(f"  ✓ logo-horizontal-{w}w.png ({w}x{h})")
    
    print("\n=== Processing VERTICAL logo ===")
    logo_v = Image.open(os.path.join(BASE, "logo-vertical.png")).convert("RGBA")
    for h in [200, 150]:
        ratio = h / logo_v.height
        w = int(logo_v.width * ratio)
        resized = logo_v.resize((w, h), Image.LANCZOS)
        path = os.path.join(BASE, f"logo-vertical-{h}h.png")
        resized.save(path, format="PNG", optimize=True)
        print(f"  ✓ logo-vertical-{h}h.png ({w}x{h})")
    
    print("\n=== Processing EMBOSS logo ===")
    logo_e = Image.open(os.path.join(BASE, "logo-emboss.png")).convert("RGBA")
    for w in [300, 200]:
        ratio = w / logo_e.width
        h = int(logo_e.height * ratio)
        resized = logo_e.resize((w, h), Image.LANCZOS)
        path = os.path.join(BASE, f"logo-emboss-{w}w.png")
        resized.save(path, format="PNG", optimize=True)
        print(f"  ✓ logo-emboss-{w}w.png ({w}x{h})")
    
    print("\n=== Processing HERO BRAND background ===")
    hero = Image.open(os.path.join(BASE, "hero-brand-bg.png")).convert("RGB")
    # Desktop hero: 1920x480
    hero_desktop = hero.resize((1920, 480), Image.LANCZOS)
    hero_desktop.save(os.path.join(BASE, "hero-brand-desktop.jpg"), format="JPEG", quality=85, optimize=True)
    print(f"  ✓ hero-brand-desktop.jpg (1920x480)")
    # Mobile: 800x600
    hero_mobile = hero.resize((800, 600), Image.LANCZOS)
    hero_mobile.save(os.path.join(BASE, "hero-brand-mobile.jpg"), format="JPEG", quality=85, optimize=True)
    print(f"  ✓ hero-brand-mobile.jpg (800x600)")
    # Full size optimized
    hero.save(os.path.join(BASE, "hero-brand-bg.jpg"), format="JPEG", quality=85, optimize=True)
    print(f"  ✓ hero-brand-bg.jpg ({hero.size[0]}x{hero.size[1]})")
    
    print("\n=== Processing BRAND SHOWCASE ===")
    showcase = Image.open(os.path.join(BASE, "brand-showcase.png")).convert("RGBA")
    showcase.save(os.path.join(BASE, "brand-showcase.png"), format="PNG", optimize=True)
    print(f"  ✓ brand-showcase.png ({showcase.size[0]}x{showcase.size[1]})")
    
    print("\n✅ All images processed successfully!")

if __name__ == "__main__":
    main()
