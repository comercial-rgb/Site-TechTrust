#!/usr/bin/env python3
from PIL import Image
import os

TARGET_WIDTH = 1920
TARGET_HEIGHT = 480

# Configuração das novas imagens - TODAS com modo FIT (mostrar imagem completa)
images = [
    {'file': 'foto-02-site-desktop-new.jpg', 'output': 'foto-02-site-desktop.png', 'fit': True},
    {'file': 'foto-03-site-desktop-new.png', 'output': 'foto-03-site-desktop.png', 'fit': True},
    {'file': 'foto-04-site-desktop-new.jpg', 'output': 'foto-04-site-desktop.png', 'fit': True},
    {'file': 'foto-05-site-desktop-new.jpg', 'output': 'foto-05-site-desktop.png', 'fit': True},
    {'file': 'foto-06-site-desktop-new.jpg', 'output': 'foto-06-site-desktop.png', 'fit': True},
    {'file': 'foto-07-site-desktop-new.jpg', 'output': 'foto-07-site-desktop.png', 'fit': True},
]

for img_cfg in images:
    img_name = img_cfg['file']
    output_name = img_cfg['output']
    crop_offset = img_cfg.get('crop_offset', 0)
    fit_mode = img_cfg.get('fit', False)

    if not os.path.exists(img_name):
        print(f"⚠️  {img_name} not found, skipping...")
        continue

    try:
        img = Image.open(img_name)
        # Converter para RGB se necessário (caso seja RGBA ou outro formato)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        original_width, original_height = img.size
        print(f"📷 Processing {img_name} ({original_width}x{original_height})...")

        aspect_ratio = original_width / original_height

        if fit_mode:
            # Ajuste para mostrar toda a imagem (fit) - mantém proporção e adiciona barras
            scale = min(TARGET_WIDTH / original_width, TARGET_HEIGHT / original_height)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_cropped = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHT), (11, 18, 32))
            paste_x = (TARGET_WIDTH - new_width) // 2
            paste_y = (TARGET_HEIGHT - new_height) // 2
            img_cropped.paste(img_resized, (paste_x, paste_y))
            print(f"   → Fit mode: scaled to {new_width}x{new_height}, centered with padding")
        else:
            # Redimensionar para cobrir toda a área (crop mode)
            scale = max(TARGET_WIDTH / original_width, TARGET_HEIGHT / original_height)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Crop vertical e horizontal para 1920x480
            if new_width > TARGET_WIDTH:
                left = (new_width - TARGET_WIDTH) // 2
            else:
                left = 0
            
            if new_height > TARGET_HEIGHT:
                # Ajuste manual de crop_offset (negativo sobe, positivo desce)
                top = max(0, ((new_height - TARGET_HEIGHT) // 2) + crop_offset)
                if top + TARGET_HEIGHT > new_height:
                    top = new_height - TARGET_HEIGHT
            else:
                top = 0
            
            img_cropped = img_resized.crop((left, top, left + TARGET_WIDTH, top + TARGET_HEIGHT))
            
            if crop_offset != 0:
                print(f"   → Crop mode with offset {crop_offset}px (top={top})")
            else:
                print(f"   → Crop mode: centered")

        # Salvar versão desktop
        img_cropped.save(output_name, 'PNG', optimize=True, quality=95)
        
        file_size = os.path.getsize(output_name) / 1024
        print(f"✅ Created {output_name} ({TARGET_WIDTH}x{TARGET_HEIGHT}, {file_size:.0f}KB)")
        
    except Exception as e:
        print(f"❌ Error processing {img_name}: {e}")

print("\n🎉 Done! New desktop images processed successfully.")
