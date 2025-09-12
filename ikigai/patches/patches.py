import os
import re
import json

# Get the directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATCHES_DIR = os.path.join(BASE_DIR, "raw")
OUTPUT_FILE = os.path.join(BASE_DIR, "info.json")

# Function to transform filename into display name
def format_name(filename: str) -> str:
    # remove prefix
    name = re.sub(r"^pokeikigai-", "", filename)
    # remove extension (.ups or .bps)
    name = re.sub(r"\.(ups|bps)$", "", name)
    # replace hyphens with spaces
    name = name.replace("-", " ")
    # split into words and capitalize (except version tags like v1, v2, etc.)
    words = []
    for word in name.split():
        if re.match(r"^v[0-9]", word):
            words.append(word)
        else:
            words.append(word.capitalize())
    return "Pokémon Ikigai " + " ".join(words)

# Collect patch info
patches = []
for filename in os.listdir(RAW_PATCHES_DIR):
    if not (filename.endswith(".ups") or filename.endswith(".bps")):
        continue
    patch_info = {
        "file": filename,
        "name": format_name(filename),
        "outputName": format_name(filename)
    }
    patches.append(patch_info)

# Final JSON structure
info = {
    "file": "./patches/ikigai.zip",
    "patches": patches
}

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Write JSON to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(info, f, indent=2, ensure_ascii=False)

# Print content (like cat)
with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    print(f.read())
