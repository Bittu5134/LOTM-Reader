import os
import re

# --- CONFIGURATION ---
# List of directories containing your images (will search subdirectories too)
IMAGE_ROOTS = [
    "images\\lotm\\backgrounds",
    "images\\lotm\\book",
    "images\\lotm\\characters",
    "images\\lotm\\vol_1",
    "images\\lotm\\vol_2",
    "images\\lotm\\vol_3",
    "images\\lotm\\vol_4",
    "images\\lotm\\vol_5",
    "images\\lotm\\vol_6",
    "images\\lotm\\vol_7",
    "images\\lotm\\vol_8",
]

# The directory containing your .md files
CONTENT_DIR = "./chapters/lotm/webnovel"


def find_unused_images():
    # 1. Gather all image filenames from subdirectories
    all_images = {}  # Filename -> Full Path
    print("Scanning image directories...")

    for root_dir in IMAGE_ROOTS:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                # You can filter by extension if needed
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
                    all_images[file] = os.path.join(root, file)

    print(f"Found {len(all_images)} total images.")

    # 2. Scan all .md files for any mention of these filenames
    used_images = set()
    md_files = []

    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))

    print(f"Analyzing {len(md_files)} Markdown files...")

    # Regex to catch standard Markdown ![]() and HTML <img src="">
    # It specifically looks for the filename at the end of a path
    image_pattern = re.compile(
        r"\/([^\/\s)]+\.(?:png|jpg|jpeg|webp|gif))", re.IGNORECASE
    )

    for md_path in md_files:
        with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            matches = image_pattern.findall(content)
            for match in matches:
                used_images.add(match)

    # 3. Compare and Report
    unused = []
    for img_name, full_path in all_images.items():
        if img_name not in used_images:
            unused.append(full_path)

    # --- OUTPUT ---
    print("\n" + "=" * 30)
    print(f"AUDIT COMPLETE")
    print(f"Total Images: {len(all_images)}")
    print(f"Used Images:  {len(used_images)}")
    print(f"Unused Images: {len(unused)}")
    print("=" * 30 + "\n")

    if unused:
        print("Unused Image Paths:")
        for path in sorted(unused):
            print(f"  [ ] {path}")
    else:
        print("All images are currently in use!")


if __name__ == "__main__":
    find_unused_images()
