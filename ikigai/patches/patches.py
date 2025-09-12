import os
import re
import json
import requests

# Get the directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATCHES_DIR = os.path.join(BASE_DIR, "raw")
PATCHES_FILE = os.path.join(BASE_DIR, "info.json")
VERSIONS_FILE = os.path.join(os.path.dirname(BASE_DIR), "versions/versions.json")

def get_release_title(tag: str, default: str) -> str:
    token = os.getenv("GITHUB_TOKEN")
    
    url = f"https://api.github.com/repos/HashtagMarky/ikigai/releases/tags/{tag}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            title = data.get("name")
            return title if title else default
        else:
            return default
    except requests.RequestException:
        return default
    
def strip_filename(filename: str) -> str:
    # Remove prefix
    name = re.sub(r"^pokeikigai-", "", filename)
    # Remove extension (.ups or .bps)
    name = re.sub(r"\.(ups|bps)$", "", name)
    # Replace hyphens with spaces
    name = name.replace("-", " ")
    # Split into words and capitalize (except version tags)
    words = [
        word if re.match(r"^v\d", word) else word.capitalize()
        for word in name.split()
    ]
    # Join back into a single string
    return " ".join(words)

def format_name(filename: str) -> str:
    # Prepend standard game name
    return "Pokémon Ikigai " + strip_filename(filename)

# Collect patch info
patches = []
for filename in os.listdir(RAW_PATCHES_DIR):
    if not (filename.endswith(".ups") or filename.endswith(".bps")):
        continue
    releaseName = get_release_title(strip_filename(filename), format_name(filename))
    patch_info = {
        "file": filename,
        "name": re.sub(r"^Pokémon Ikigai ", "", releaseName),
        "outputName": releaseName
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
    name_without_prefix = patch["file"].removeprefix("Pokémon Ikigai ").strip()
    manifest_entry = {
        "name": re.sub(r"^Pokémon Ikigai ", "", get_release_title(name_without_prefix, patch["name"])),
        "file": f"{strip_filename(name_without_prefix)}.md",
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
