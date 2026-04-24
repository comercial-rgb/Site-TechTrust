#!/usr/bin/env python3
from PIL import Image
import os

TARGET_WIDTH = 1920
TARGET_HEIGHT = 480

# Configuração especial para crop manual
images = [
    {'file': 'foto-02-site.png'},
    {'file': 'foto-03-site.png', 'crop_offset': -120},  # valor negativo sobe o crop para mostrar mais o rosto
    {'file': 'foto-04-site.jpg'},
    {'file': 'foto-05-site.png'},
    {'file': 'foto-06-site.png'},
    {'file': 'foto-07-site.png', 'fit': True},  # fit: mostra toda a imagem, com barras se necessário
]

for img_cfg in images:
    if isinstance(img_cfg, str):
        img_cfg = {'file': img_cfg}
    img_name = img_cfg['file']
    crop_offset = img_cfg.get('crop_offset', 0)
    fit_mode = img_cfg.get('fit', False)

    if not os.path.exists(img_name):
        print(f"⚠️  {img_name} not found, skipping...")
        continue

    try:
        img = Image.open(img_name)
        original_width, original_height = img.size
        print(f"📷 Processing {img_name} ({original_width}x{original_height})...")

        aspect_ratio = original_width / original_height

        if fit_mode:
            # Ajuste para mostrar toda a imagem (fit)
            scale = min(TARGET_WIDTH / original_width, TARGET_HEIGHT / original_height)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_cropped = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHT), (11, 18, 32))
            paste_x = (TARGET_WIDTH - new_width) // 2
            paste_y = (TARGET_HEIGHT - new_height) // 2
            img_cropped.paste(img_resized, (paste_x, paste_y))
        else:
            # Redimensionar para largura mínima
            if original_width < TARGET_WIDTH:
                new_width = TARGET_WIDTH
                new_height = int(TARGET_WIDTH / aspect_ratio)
            else:
                new_width = original_width
                new_height = original_height
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Crop vertical (ajuste manual se crop_offset)
            if new_height > TARGET_HEIGHT:
                top = max(0, ((new_height - TARGET_HEIGHT) // 2) + crop_offset)
                if top + TARGET_HEIGHT > new_height:
                    top = new_height - TARGET_HEIGHT
                img_cropped = img_resized.crop((0, top, TARGET_WIDTH, top + TARGET_HEIGHT))
            else:
                img_cropped = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHT), (11, 18, 32))
                paste_y = (TARGET_HEIGHT - new_height) // 2
                img_cropped.paste(img_resized, (0, paste_y))

        output_name = img_name.replace('.png', '-desktop.png').replace('.jpg', '-desktop.png')
        img_cropped.save(output_name, 'PNG', optimize=True, quality=95)
        print(f"✅ Created {output_name} (1920x480)")


        
    except Exception as e:
        print(f"❌ Error processing {img_name}: {e}")

print("\n🎉 Done! Desktop images created successfully.")
