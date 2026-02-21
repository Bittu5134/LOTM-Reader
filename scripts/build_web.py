import os
import re
import asyncio
import json
import shutil
import imagesize
from pathlib import Path
import frontmatter

# --- CONFIGURATION ---

# Where your .webp images are physically located on your machine for sizing
IMG_STORAGE_DIR = Path("website/static/assets/images")

# The URL path the browser will use to fetch images
IMG_PUBLIC_PREFIX = "/assets/images"

TEMPLATE_PATH = Path("website/src/lib/reader/template.svelte")
META_OUTPUT_PATH = Path("website/src/lib/meta.json")
OUTPUT_ROOT = Path("website/src/routes/(reader)/read/")

MAX_CONCURRENT_TASKS = 75
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

completed_count = 0

# --- LOGGING HELPERS ---


def gh_log(message):
    print(message)


def gh_group(title):
    print(f"::group::{title}")


def gh_endgroup():
    print("::endgroup::")


# --- CORE LOGIC ---


def process_html_images(html_content):
    """
    Finds img tags, preserves subfolder structure after 'images/',
    changes extension to webp, reads dimensions, and injects width/height.
    """

    def replacer(match):
        full_tag = match.group(0)

        # Extract src using regex
        src_match = re.search(r'src=["\'](.*?)["\']', full_tag)
        if not src_match:
            return full_tag  # Skip malformed tags

        old_path = src_match.group(1)

        # 1. Parse Path & Preserve Subfolders
        # Normalize slashes to forward slashes for splitting
        normalized_path = old_path.replace("\\", "/")

        # Logic: If path is `../../images/sub/folder/img.jpg`, we want `sub/folder/img.webp`
        if "/images/" in normalized_path:
            # Split by /images/ and take the last part
            relative_part = normalized_path.split("/images/")[-1]
        elif "images/" in normalized_path:
            # Handle case where path starts with images/
            relative_part = normalized_path.split("images/")[-1]
        else:
            # Fallback: If 'images' keyword missing, just take the filename
            relative_part = Path(old_path).name

        # Convert extension to .webp (using Path for easy suffix handling)
        rel_path_obj = Path(relative_part).with_suffix(".webp")

        # 2. Construct New Web URL (Must use forward slashes)
        new_src = f"{IMG_PUBLIC_PREFIX}/{rel_path_obj.as_posix()}"

        # 3. Construct Local File Path for sizing (OS-agnostic)
        local_file_path = IMG_STORAGE_DIR / rel_path_obj

        width_attr = ""
        height_attr = ""

        if local_file_path.exists():
            try:
                w, h = imagesize.get(local_file_path)
                width_attr = f' width={w}'
                height_attr = f' height={h}'
            except:
                pass  # Fail silently
        else:
            # Only warn if we can't find it (helps debug missing folders)
            gh_log(f"::warning::Image not found at expected path: {local_file_path}")

        # 4. Reconstruct Tag
        new_tag = re.sub(r'src=["\'].*?["\']', f'src="{new_src}"', full_tag)

        if "/>" in new_tag:
            new_tag = new_tag.replace("/>", f"{width_attr}{height_attr} />")
        else:
            new_tag = new_tag.replace(">", f"{width_attr}{height_attr}>")

        return new_tag

    return re.sub(r"<img\s+[^>]*?>", replacer, html_content, flags=re.DOTALL)


async def convert_chapter(
    post_content, post_meta, output_file, total_tasks, template_str
):
    global completed_count

    async with semaphore:
        process = await asyncio.create_subprocess_exec(
            "pandoc",
            "-f",
            "markdown",
            "-t",
            "html",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate(input=post_content.encode("utf-8"))

        if stderr:
            gh_log(
                f"Pandoc Error for {post_meta.get('title', 'Unknown')}: {stderr.decode()}"
            )

        html_content = stdout.decode("utf-8")

        # Process Images
        html_content = process_html_images(html_content)

        # Inject HTML into the Svelte template
        # FIX: Correctly target the placeholder
        final_svelte_content = template_str.replace("<!-- [DATA] -->", html_content)

        # Inject Metadata
        final_svelte_content = final_svelte_content.replace(
            "// [METADATA]", f"let ch_meta = {json.dumps(post_meta)}"
        )

        # Cleanup
        final_svelte_content = final_svelte_content.replace("// [IMG_IMPORT]", "")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_svelte_content)

        completed_count += 1
        if completed_count % 50 == 0 or completed_count == total_tasks:
            gh_log(f"Progress: [{completed_count}/{total_tasks}]")


async def main():
    paths = [
        "./chapters/lotm/webnovel/",
        "./chapters/lotm/oldtl/",
        "./chapters/coi/webnovel/",
    ]

    gh_group("Initialization")

    if not TEMPLATE_PATH.exists():
        gh_log(f"::error::Template not found at {TEMPLATE_PATH}")
        exit(1)

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template_str = f.read()

    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
        gh_log("Cleaned previous output directory.")

    tasks_data = []
    meta_map = {}

    gh_endgroup()

    gh_group("Indexing Chapters")

    for path in paths:
        if not os.path.exists(path):
            gh_log(f"Skipping: {path} (Not found)")
            continue

        master_path = os.path.join(path, "0000.md")
        if not os.path.exists(master_path):
            gh_log(f"Skipping: {path} (0000.md missing)")
            continue

        masterMD = frontmatter.load(master_path)
        bookID, bookTL = masterMD["metaBook"], masterMD["metaTl"].lower()

        if bookID not in meta_map:
            meta_map[bookID] = {}
        if bookTL not in meta_map[bookID]:
            meta_map[bookID][bookTL] = []

        files = [f for f in os.listdir(path) if f.endswith(".md") and f != "0000.md"]
        gh_log(f"Found {len(files)} chapters for {bookID} ({bookTL})")

        for file in files[:30]:
            post = frontmatter.load(os.path.join(path, file))
            slug = post.metadata.get("slug")
    
            # Simple header fix
            post.content = re.sub(r"^#(#+)", r"\1", post.content, flags=re.MULTILINE)

            if not slug:
                continue

            meta_map[bookID][bookTL].append(post.metadata)

            # Ensure path components are strings
            output_dir = OUTPUT_ROOT / str(bookID) / str(bookTL) / str(slug)
            output_dir.mkdir(parents=True, exist_ok=True)

            tasks_data.append(
                {
                    "content": post.content,
                    "meta": post.metadata,
                    "dest": output_dir / "+page.svelte",
                }
            )

    # Save Meta JSON
    with open(META_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(meta_map, f, indent=2)

    gh_endgroup()

    total = len(tasks_data)
    gh_group(f"Processing {total} Chapters")

    tasks = [
        convert_chapter(td["content"], td["meta"], td["dest"], total, template_str)
        for td in tasks_data
    ]

    await asyncio.gather(*tasks)

    gh_endgroup()
    gh_log("Build Complete.")


if __name__ == "__main__":
    asyncio.run(main())
