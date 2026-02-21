import os
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# ... (Configuration and Logging Helper remain the same) ...
# ============================================================
# CONFIGURATION
# ============================================================
SOURCE_DIR = "./images"
DEST_DIR = "./website/static/assets/images"


def gh_log(msg, type="info"):
    """Format logs for GitHub Actions UI"""
    if type == "group":
        print(f"::group::{msg}", flush=True)
    elif type == "endgroup":
        print("::endgroup::", flush=True)
    elif type == "error":
        print(f"::error::{msg}", flush=True)
    else:
        print(msg, flush=True)


# ============================================================
# IMAGE PROCESSOR
# ============================================================
def process_image(paths):
    """
    - If WebP: Copy file directly.
    - If Other: Convert to WebP and save.
    """
    input_path, relative_path = paths
    filename = os.path.basename(input_path)

    # Calculate output path (Always ends in .webp)
    name_no_ext, ext = os.path.splitext(relative_path)
    webp_rel_path = name_no_ext + ".webp"
    output_path = os.path.join(DEST_DIR, webp_rel_path)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        # CASE 1: Already WebP -> Copy only
        if ext.lower() == ".webp":
            shutil.copy2(input_path, output_path)
            return f"⏩ Copied: {filename}"

        # CASE 2: Not WebP -> Convert to WebP
        # (This creates a NEW file at output_path; original is ignored)
        cmd = [
            "magick",
            input_path,
            "-quality",
            "85",
            "-define",
            "webp:method=6",
            "-strip",
            output_path,
        ]

        subprocess.run(cmd, check=True, capture_output=True)
        return f"✅ Converted: {filename}"

    except subprocess.CalledProcessError as e:
        return f"❌ ERROR {filename}: {e.stderr.decode().strip()}"
    except Exception as e:
        return f"❌ CRITICAL {filename}: {str(e)}"


# ... (Main Pipeline remains the same) ...
# ============================================================
# MAIN PIPELINE
# ============================================================
def run_pipeline():
    gh_log("📷 Starting Image Optimization Pipeline", "group")

    valid_exts = (".jpg", ".jpeg", ".png", ".tiff", ".webp", ".avif")
    tasks = []

    if not os.path.exists(SOURCE_DIR):
        gh_log(f"Source directory {SOURCE_DIR} not found.", "error")
        return

    print(f"Scanning {SOURCE_DIR}...")
    for subdir, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith(valid_exts):
                full_path = os.path.join(subdir, file)
                rel_path = os.path.relpath(full_path, SOURCE_DIR)
                tasks.append((full_path, rel_path))

    if not tasks:
        gh_log("No images found.", "info")
        gh_log("", "endgroup")
        return

    print(f"Found {len(tasks)} images. Processing with {os.cpu_count()} cores...")
    gh_log("", "endgroup")

    gh_log(f"Processing {len(tasks)} Images...", "group")

    with ProcessPoolExecutor() as executor:
        future_to_image = {executor.submit(process_image, task): task for task in tasks}

        for i, future in enumerate(as_completed(future_to_image)):
            result = future.result()
            if "ERROR" in result or "CRITICAL" in result:
                gh_log(result, "error")
            elif i % 10 == 0:
                print(f"[{i+1}/{len(tasks)}] {result}", flush=True)

    gh_log("All images processed successfully.", "endgroup")


if __name__ == "__main__":
    run_pipeline()
