import os
import frontmatter
import sys

# --- CONFIGURATION ---
SOURCE_DIR = "./chapters/lotm/webnovel"  # Where to copy FROM
TARGET_DIR = "./chapters/lotm/oldtl"  # Where to copy TO


def sync_discussion_key():
    # Get list of md files
    try:
        files = sorted([f for f in os.listdir(SOURCE_DIR) if f.endswith(".md") and f != "0000.md"])
    except FileNotFoundError:
        print(f"Error: Source directory '{SOURCE_DIR}' not found.")
        return

    print(f"{'STATUS':<10} | {'FILENAME'}")
    print("=" * 50)

    count_updated = 0
    count_skipped = 0
    count_missing = 0

    for filename in files:
        path1 = os.path.join(SOURCE_DIR, filename)
        path2 = os.path.join(TARGET_DIR, filename)

        # 1. Check if file exists in Target
        if not os.path.exists(path2):
            count_missing += 1
            continue

        try:
            # 2. Load both files
            post1 = frontmatter.load(path1)
            post2 = frontmatter.load(path2)

            # 3. Check if Source has 'discussion' key
            if "discussion" in post1.metadata:
                discussion_value = post1.metadata["discussion"]

                # 4. Check if we actually need to update (avoid useless writes)
                current_value = post2.metadata.get("discussion")

                if current_value != discussion_value:
                    # Copy the key/value over
                    post2.metadata["discussion"] = discussion_value

                    # Write back to Target file
                    with open(path2, "wb") as f:
                        frontmatter.dump(post2, f)

                    print(f"✅ UPDATED  | {filename}")
                    count_updated += 1
                else:
                    # Value is already same
                    count_skipped += 1
            else:
                # Source file doesn't have a discussion key
                count_skipped += 1

        except Exception as e:
            print(f"❌ ERROR    | {filename} - {e}")

    print("\n" + "=" * 40)
    print("SYNC COMPLETE")
    print("=" * 40)
    print(f"Files Updated: {count_updated}")
    print(f"Files Skipped: {count_skipped} (No change/No key)")
    print(f"Missing in Tgt:{count_missing}")
    print("=" * 40)


if __name__ == "__main__":
    # Optional: Allow command line args like: python script.py ./src ./dest
    if len(sys.argv) == 3:
        SOURCE_DIR = sys.argv[1]
        TARGET_DIR = sys.argv[2]

    sync_discussion_key()
