#!/usr/bin/env python3
"""
renamer.py
Pass a screenshot path, get back a hyphenated tag.
Usage: uv run python3 renamer.py ~/Desktop/yourscreenshot.png
"""

import sys
import base64
import io
import json
import re
import urllib.request
import urllib.error
from PIL import Image # make sure you have pillow installed :)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "hf.co/Qwen/Qwen3-VL-2B-Instruct-GGUF:Q4_K_M" # Any model here
MAX_EDGE = 768 # Modify based on hardware


def encode_image(image_path: str) -> str:
    with Image.open(image_path) as img:
        w, h = img.size
        if max(w, h) > MAX_EDGE:
            scale = MAX_EDGE / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")


def tag_screenshot(image_path: str) -> str:
    b64 = encode_image(image_path)

    payload = {
        "model": MODEL,
        "system": "You are a file renamer. Output only a hyphenated-lowercase-tag.",
        "prompt": "Tag this screenshot in 3-5 words. Prioritize what you see rather than the specific text", # You can tweak this prompt to make it better!
        "images": [b64],
        "stream": False,
        "options": {"num_ctx": 8192, "num_predict": 4096},
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.load(resp)

    tag = result.get("response", "").strip()
    tag = tag.lower()
    tag = re.sub(r"[^a-z0-9\-]", "-", tag)
    tag = re.sub(r"-+", "-", tag).strip("-")
    tag = tag[:50]

    return tag


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 renamer.py <path-to-image>")
        sys.exit(1)

    path = sys.argv[1]

    print(f"Model  : {MODEL}")
    print(f"Image  : {path}")
    print("Tagging...\n")

    try:
        tag = tag_screenshot(path)
        print(f"Tag    : {tag}")
    except urllib.error.URLError:
        print("Error: Could not reach Ollama. Is it running? Try: ollama serve")
    except FileNotFoundError:
        print(f"Error: File not found — {path}")
