"""Remove white/light-gray backgrounds from logo images and regenerate web sizes."""
from PIL import Image
import numpy as np
import shutil

THRESHOLD = 230  # pixels with R,G,B all > this are background

def remove_bg(path, threshold=THRESHOLD):
    """Remove near-white background, replacing with transparency."""
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    
    # Identify near-white/light pixels
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
    bg_mask = (r > threshold) & (g > threshold) & (b > threshold)
    
    # Use flood-fill approach from corners to only remove connected background
    from scipy import ndimage
    # Label connected components in the background mask
    labeled, num = ndimage.label(bg_mask)
    
    # Find labels that touch any edge
    edge_labels = set()
    h, w = labeled.shape
    edge_labels.update(labeled[0, :].tolist())      # top
    edge_labels.update(labeled[-1, :].tolist())     # bottom
    edge_labels.update(labeled[:, 0].tolist())      # left
    edge_labels.update(labeled[:, -1].tolist())     # right
    edge_labels.discard(0)  # 0 = non-background
    
    # Only make edge-connected white regions transparent
    final_mask = np.zeros_like(bg_mask)
    for lbl in edge_labels:
        final_mask |= (labeled == lbl)
    
    # Apply transparency with anti-aliasing at edges
    # For pixels on the border of the mask, use partial transparency
    from scipy.ndimage import binary_dilation
    dilated = binary_dilation(final_mask, iterations=1)
    border = dilated & ~final_mask
    
    arr[final_mask, 3] = 0  # Fully transparent
    # Border pixels get partial transparency for smoother edges
    for y, x in zip(*np.where(border)):
        luminance = (int(arr[y,x,0]) + int(arr[y,x,1]) + int(arr[y,x,2])) / 3
        if luminance > threshold:
            arr[y, x, 3] = max(0, int(255 - (luminance - threshold) * (255 / (255 - threshold))))
    
    result = Image.fromarray(arr)
    return result


def process_and_save(src, dest, threshold=THRESHOLD):
    """Remove background and save."""
    img = remove_bg(src, threshold)
    img.save(dest, 'PNG', optimize=True)
    print(f"  ✓ {dest} ({img.size[0]}x{img.size[1]})")
    return img


def resize_height(img, h):
    ratio = h / img.height
    w = int(img.width * ratio)
    return img.resize((w, h), Image.LANCZOS)


def resize_width(img, w):
    ratio = w / img.width
    h = int(img.height * ratio)
    return img.resize((w, h), Image.LANCZOS)


if __name__ == '__main__':
    try:
        from scipy import ndimage
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'scipy', '-q'])
        from scipy import ndimage
    
    print("=== Removing backgrounds from logos ===\n")
    
    # 1. Logo Vertical
    print("Logo Vertical:")
    vert = process_and_save('logo-vertical.png', 'logo-vertical.png')
    v200 = resize_height(vert, 200)
    v200.save('logo-vertical-200h.png', 'PNG', optimize=True)
    print(f"  ✓ logo-vertical-200h.png ({v200.size[0]}x{v200.size[1]})")
    v150 = resize_height(vert, 150)
    v150.save('logo-vertical-150h.png', 'PNG', optimize=True)
    print(f"  ✓ logo-vertical-150h.png ({v150.size[0]}x{v150.size[1]})")
    
    # 2. Logo Horizontal
    print("\nLogo Horizontal:")
    horiz = process_and_save('logo-horizontal.png', 'logo-horizontal.png')
    for w in [400, 300, 200]:
        h = resize_width(horiz, w)
        name = f'logo-horizontal-{w}w.png'
        h.save(name, 'PNG', optimize=True)
        print(f"  ✓ {name} ({h.size[0]}x{h.size[1]})")
    
    # 3. Logo Emboss (has slightly darker bg ~237)
    print("\nLogo Emboss:")
    emb = process_and_save('logo-emboss.png', 'logo-emboss.png', threshold=225)
    for w in [300, 200]:
        e = resize_width(emb, w)
        name = f'logo-emboss-{w}w.png'
        e.save(name, 'PNG', optimize=True)
        print(f"  ✓ {name} ({e.size[0]}x{e.size[1]})")
    
    # Copy to public/
    import os
    pub = 'public'
    for f in os.listdir('.'):
        if f.startswith(('logo-vertical','logo-horizontal','logo-emboss')) and f.endswith('.png'):
            shutil.copy2(f, os.path.join(pub, f))
    
    print("\n✅ All logos processed with transparent backgrounds!")
    
    # Verify
    for f in ['logo-vertical-200h.png', 'logo-horizontal-300w.png', 'logo-emboss-300w.png']:
        img = Image.open(f)
        arr = np.array(img)
        alpha_min = arr[:,:,3].min()
        transparent_pct = (arr[:,:,3] == 0).sum() / (arr.shape[0]*arr.shape[1]) * 100
        print(f"  {f}: transparent pixels = {transparent_pct:.1f}%")
