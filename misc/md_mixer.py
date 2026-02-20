import os
import re
import sys
import frontmatter

# --- CONFIGURATION ---
DIR_A = "./chapters/lotm/webnovel"  # Source (New TL with Images/Notes)
DIR_B = "./chapters/lotm/oldtl"  # Target (Old TL to be updated)


def clean_version_A(text):
    """Cleans New TL: Removes Images, Pandoc Footnotes."""
    if not text:
        return ""
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text, flags=re.DOTALL)
    text = re.sub(r"<img[^>]+>", "", text, flags=re.DOTALL)
    text = re.sub(r"\^\[.*?\]", "", text, flags=re.DOTALL)
    text = re.sub(r"\[\^.*?\]", "", text)
    return text


def clean_version_B(text):
    """Cleans Old TL: Removes legacy numbered blocks and link refs."""
    if not text:
        return ""
    text = re.sub(r"(?m)^\s*\d+\.\s*\[[\s\S]*?\]", "", text)
    text = re.sub(r"\[\\?\[\d+\\?\]\]\(#.*?\)", "", text)
    return text


def normalize_alphabets_only(text):
    """Nuclear option: Keep only a-z."""
    if not text:
        return ""
    return re.sub(r"[^a-zA-Z]", "", text).lower()


def get_features_in_A(text):
    """Returns list of tags (IMG, FN) if present."""
    tags = []
    if re.search(r"!\[.*?\]\(.*?\)|<img[^>]+>", text, re.DOTALL):
        tags.append("IMG")
    if re.search(r"\^\[.*?\]|\[\^.*?\]", text):
        tags.append("FN")
    return tags


def run_sync(dir1, dir2):
    files = sorted([f for f in os.listdir(dir1) if f.endswith(".md")])

    print(f"{'STATUS':<10} | {'FEATURES':<10} | {'FILENAME'}")
    print("=" * 80)

    count_updated = 0
    count_diff = 0
    count_skipped = 0

    for filename in files:
        path1 = os.path.normpath(os.path.join(dir1, filename))
        path2 = os.path.normpath(os.path.join(dir2, filename))

        if not os.path.exists(path2):
            continue

        try:
            # Load Files
            p1 = frontmatter.load(path1)
            p2 = frontmatter.load(path2)
            raw1 = p1.content or ""
            raw2 = p2.content or ""

            # 1. Check if Source has features (Images/Notes)
            features = get_features_in_A(raw1)
            if not features:
                count_skipped += 1
                continue

            feature_str = "+".join(features)

            # 2. Clean & Compare
            cleaned_A = clean_version_A(raw1)
            cleaned_B = clean_version_B(raw2)
            norm_A = normalize_alphabets_only(cleaned_A)
            norm_B = normalize_alphabets_only(cleaned_B)

            # 3. ACTION LOGIC
            if norm_A == norm_B:
                # SAFE MATCH: Overwrite Content
                # We update p2's content with p1's content (which includes the images/notes)
                # We KEEP p2's metadata (frontmatter) as is.
                p2.content = p1.content

                # Write back to file B
                with open(path2, "wb") as f:
                    frontmatter.dump(p2, f)

                count_updated += 1
                # No print needed for success, keeping console clean

            else:
                # REAL DIFF: Manual Check Needed
                print(f"❌ DIFF     | {feature_str:<10} | {filename}")
                print(f"   A (Src): {path1}")
                print(f"   B (Tgt): {path2}")
                print("-" * 50)
                count_diff += 1

        except Exception as e:
            print(f"ERROR: {filename} - {e}")

    print("\n" + "=" * 40)
    print("SYNC COMPLETE")
    print("=" * 40)
    print(f"Files Auto-Updated (Safe Copy): {count_updated}")
    print(f"Files Requiring Manual Check:   {count_diff}")
    print(f"Files Skipped (No Media):       {count_skipped}")
    print("=" * 40)


if __name__ == "__main__":
    run_sync(DIR_A, DIR_B)
