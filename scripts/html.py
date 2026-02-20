import os
import re
import asyncio
import frontmatter
import json  # Added for json export
from pathlib import Path

# Limit concurrent processes to avoid OS overload
MAX_CONCURRENT_TASKS = 75
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

# Path to your Svelte template
TEMPLATE_PATH = Path("website/src/lib/template.svelte")
# Path for the generated metadata
META_OUTPUT_PATH = Path("website/src/lib/meta.json")

# Counter for global progress tracking
completed_count = 0


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

        if not stderr:
            img_imports = []
            html_content = stdout.decode("utf-8")
            image_paths = re.findall(r'<img\s+[^>]*src=["\'](.*?)["\']', html_content, flags=re.DOTALL)
            for img_path in image_paths:
                img_var = img_path.replace("../../../images/", "chapter_images_")
                img_var = re.sub(r"[\\/.]", "_", img_var)
                html_content = html_content.replace(img_path, "{" + img_var + "}")
                img_imports.append(
                    f"import {img_var} from '$lib/{img_path[9:]}?enhanced'"
                )
            html_content = html_content.replace("<img", "<enhanced:img")

            # Inject HTML into the Svelte template
            final_svelte_content: str = template_str.replace(
                "<!-- [DATA] -->", html_content
            )
            final_svelte_content = final_svelte_content.replace(
                "// [IMG_IMPORT]", "\n".join(img_imports)
            )

            # Using json.dumps ensures Python True/None becomes JS true/null
            final_svelte_content = final_svelte_content.replace(
                "// [METADATA]", f"let ch_meta = {json.dumps(post_meta)}"
            )

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(final_svelte_content)

            completed_count += 1
            if completed_count % 10 == 0 or completed_count == total_tasks:
                print(
                    f"Progress: [{completed_count}/{total_tasks}] chapters converted...",
                    end="\r",
                )


async def main():
    paths = [
        "./chapters/lotm/webnovel/",
        "./chapters/lotm/oldtl/",
        "./chapters/coi/webnovel/",
    ]

    # 1. Load the template file
    if not TEMPLATE_PATH.exists():
        print(f"CRITICAL ERROR: Template not found at {TEMPLATE_PATH}")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template_str = f.read()

    tasks_data = []
    meta_map = {}  # Object to store lotm/coi info

    print("--- Initializing Build ---")

    for path in paths:
        if not os.path.exists(path):
            print(f"Skipping: {path} (Not found)")
            continue

        # Load book metadata from 0000.md
        masterMD = frontmatter.load(os.path.join(path, "0000.md"))
        bookID, bookTL = masterMD["metaBook"], masterMD["metaTl"].lower()

        # Initialize meta_map for this book and translation
        if bookID not in meta_map:
            meta_map[bookID] = {}
        if bookTL not in meta_map[bookID]:
            meta_map[bookID][bookTL] = []

        files = [f for f in os.listdir(path) if f.endswith(".md") and f != "0000.md"]

        print(f"Indexing {len(files)} chapters from {bookID} ({bookTL})...")

        for file in files:
            post = frontmatter.load(os.path.join(path, file))
            slug = post.metadata.get("slug")
            post.content = re.sub(r"^#(#+)", r"\1", post.content, flags=re.MULTILINE)
            if not slug:
                continue

            # Add chapter info to our meta_map
            meta_map[bookID][bookTL].append(post.metadata)

            output_dir = Path(
                f"website/src/routes/(reader)/read/{bookID}/{bookTL}/{slug}"
            )
            output_dir.mkdir(parents=True, exist_ok=True)

            tasks_data.append(
                {
                    "content": post.content,
                    "meta": post.metadata,
                    "dest": output_dir / "+page.svelte",
                }
            )

    # Save the consolidated meta.json
    with open(META_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(meta_map, f, indent=2)
    print(f"--- Meta JSON generated at {META_OUTPUT_PATH} ---")

    # test_tasks_data = tasks_data[:300]
    test_tasks_data = tasks_data
    total = len(test_tasks_data)

    print(f"\n--- Starting Conversion of {total} chapters using template ---")

    tasks = [
        convert_chapter(td["content"], td["meta"], td["dest"], total, template_str)
        for td in test_tasks_data
    ]

    await asyncio.gather(*tasks)
    print(f"\n\nDone! Successfully generated {total} SvelteKit routes and meta.json.")


if __name__ == "__main__":

    asyncio.run(main())
