# ============================================================
# ROMANTIC PHOTO EDITOR — Stable Diffusion Img2Img
# Face-preserving + atmospheric romantic edit
# ============================================================
import os
import json
import torch
import random
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline

# ============================================================
# KONFIGURASI
# ============================================================
INPUT_DIR = "input"
OUTPUT_DIR = "output"
CONFIG_FILE = "config.json"

# Default config
DEFAULT_CONFIG = {
    "strength": 0.20,
    "guidance_scale": 7.5,
    "num_inference_steps": 30,
    "max_size": 768,
    "prompt": (
        "romantic warm atmosphere, golden hour lighting, "
        "soft fairy lights in background, gentle warm glow, "
        "cinematic color grading, pink and gold tones, "
        "soft bokeh, cozy intimate moment, "
        "photorealistic, high quality, soft warm lighting, "
        "preserve original face, keep identity, natural skin tone"
    ),
    "negative_prompt": (
        "dark, cold, blue tones, ugly, blurry, deformed, "
        "distorted, low quality, bad anatomy, extra limbs, "
        "extra fingers, mutation, watermark, text, signature, "
        "different face, changed identity, plastic skin"
    ),
}

# Override from env
if os.environ.get("STRENGTH"):
    DEFAULT_CONFIG["strength"] = float(os.environ["STRENGTH"])

# Load config.json kalau ada
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as f:
        user_config = json.load(f)
        DEFAULT_CONFIG.update(user_config)
        print(f"Config loaded from {CONFIG_FILE}")

CFG = DEFAULT_CONFIG
print(f"\n⚙️  Config:")
for k, v in CFG.items():
    if isinstance(v, str) and len(v) > 60:
        v = v[:60] + "..."
    print(f"   {k}: {v}")

# ============================================================
# SETUP FOLDERS
# ============================================================
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# LOAD MODEL
# ============================================================
print("\n📦 Loading Stable Diffusion 1.5 (CPU)...")
print("   Model size: ~4 GB (first run)")

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32,
    safety_checker=None,
    requires_safety_checker=False,
)

pipe = pipe.to("cpu")
pipe.enable_attention_slicing()
print("✅ Model loaded")

# ============================================================
# PROCESS IMAGES
# ============================================================
files = [
    f for f in os.listdir(INPUT_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
]
files.sort()

print(f"\n📸 Found {len(files)} image(s)")

if len(files) == 0:
    print("❌ No images in input/ folder")
    exit(1)

for idx, fname in enumerate(files, 1):
    print(f"\n{'='*60}")
    print(f"[{idx}/{len(files)}] {fname}")
    print('='*60)

    try:
        # Load image
        img_path = os.path.join(INPUT_DIR, fname)
        img = Image.open(img_path).convert("RGB")
        orig_size = img.size
        print(f"   Original size: {orig_size}")

        # Resize kalau terlalu besar
        if max(img.size) > CFG["max_size"]:
            ratio = CFG["max_size"] / max(img.size)
            new_size = tuple(int(d * ratio) for d in img.size)
            img = img.resize(new_size, Image.LANCZOS)
            print(f"   Resized to: {new_size}")

        # Seed random (biar hasil beda setiap run)
        seed = random.randint(0, 2**32 - 1)
        generator = torch.Generator("cpu").manual_seed(seed)
        print(f"   Seed: {seed}")

        # Generate
        print(f"   🎨 Generating (strength={CFG['strength']}, steps={CFG['num_inference_steps']})...")
        print(f"   ⏳ This takes 5-15 minutes on CPU...")

        result = pipe(
            prompt=CFG["prompt"],
            negative_prompt=CFG["negative_prompt"],
            image=img,
            strength=CFG["strength"],
            guidance_scale=CFG["guidance_scale"],
            num_inference_steps=CFG["num_inference_steps"],
            generator=generator,
        ).images[0]

        # Save
        base_name = os.path.splitext(fname)[0]
        out_name = f"romantic_{base_name}.png"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        result.save(out_path)

        size_kb = os.path.getsize(out_path) / 1024
        print(f"   ✅ Saved: {out_name} ({size_kb:.1f} KB)")

    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*60}")
print("✅ ALL DONE")
print('='*60)
print(f"Results in: {OUTPUT_DIR}/")
for f in os.listdir(OUTPUT_DIR):
    print(f"   - {f}")
