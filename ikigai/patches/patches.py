import os
import re
import json

# Get the directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATCHES_DIR = os.path.join(BASE_DIR, "raw")
PATCHES_FILE = os.path.join(BASE_DIR, "info.json")
VERSIONS_FILE = os.path.join(os.path.dirname(BASE_DIR), "versions/versions.json")

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
os.makedirs(os.path.dirname(PATCHES_FILE), exist_ok=True)

# Write JSON to file
with open(PATCHES_FILE, "w", encoding="utf-8") as f:
    json.dump(info, f, indent=2, ensure_ascii=False)

# Print content (like cat)
with open(PATCHES_FILE, "r", encoding="utf-8") as f:
    print("\nPatches File")
    print(f.read())

manifest = []
for patch in patches:
    name_without_prefix = patch["name"].removeprefix("Pokémon Ikigai ").strip()
    manifest_entry = {
        "name": patch["name"],
        "file": f"{name_without_prefix}.md",
        "patch": patch["file"]
    }
    manifest.append(manifest_entry)

# Write manifest JSON to file
with open(VERSIONS_FILE, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# Print content (like cat)
with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
    print("\nVersions File")
    print(f.read())
