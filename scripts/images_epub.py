import os
import logging
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
SOURCE_DIR = "./images"
WEBP_DIR = "./images_default"
JPEG_DIR = "./images_legacy"


# ============================================================
# LOGGING HELPER (GitHub Actions)
# ============================================================
def gh_log(msg, type="info"):
    """
    Format logs for GitHub Actions UI.
    - group: Creates a collapsible section.
    - error: Highlights text in red.
    - warning: Highlights text in yellow.
    """
    if type == "group":
        print(f"::group::{msg}", flush=True)
    elif type == "endgroup":
        print("::endgroup::", flush=True)
    elif type == "error":
        print(f"::error::{msg}", flush=True)
    elif type == "warning":
        print(f"::warning::{msg}", flush=True)
    else:
        print(msg, flush=True)


# ============================================================
# WORKER FUNCTION
# ============================================================
def process_image_suite(paths):
    """Processes a single image: Converts to WebP and B&W JPEG."""
    input_path, relative_path = paths
    filename = os.path.basename(input_path)

    # Define paths for the converted versions
    webp_path = os.path.join(WEBP_DIR, os.path.splitext(relative_path)[0] + ".webp")
    jpeg_path = os.path.join(JPEG_DIR, os.path.splitext(relative_path)[0] + ".jpg")

    # Ensure directories exist
    os.makedirs(os.path.dirname(webp_path), exist_ok=True)
    os.makedirs(os.path.dirname(jpeg_path), exist_ok=True)

    try:
        # 1. WebP Conversion (High Quality, Color)
        cmd_webp = [
            "magick",
            input_path,
            "-resize",
            "2000x2000>",
            "-quality",
            "85",
            "-define",
            "webp:method=6",
            "-define",
            "webp:lossless=false",
            "-strip",
            webp_path,
        ]
        subprocess.run(cmd_webp, check=True, capture_output=True)

        # 2. JPEG B&W Conversion (Smaller, Grayscale)
        cmd_jpeg = [
            "magick",
            input_path,
            "-resize",
            "750x750>",
            "-colorspace",
            "gray",
            "-normalize",
            "-quality",
            "75",
            "-strip",
            jpeg_path,
        ]
        subprocess.run(cmd_jpeg, check=True, capture_output=True)

        return {"status": "success", "file": filename}

    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.decode().strip() if e.stderr else str(e)
        return {"status": "error", "file": filename, "msg": err_msg}

    except Exception as e:
        return {"status": "critical", "file": filename, "msg": str(e)}


# ============================================================
# MAIN PIPELINE
# ============================================================
def run_pipeline():
    start_time = time.time()
    gh_log("🚀 Starting Image Processing Pipeline", "group")

    valid_exts = (".jpg", ".jpeg", ".png", ".tiff", ".webp")
    tasks = []

    if not os.path.exists(SOURCE_DIR):
        gh_log(f"Source directory {SOURCE_DIR} not found.", "error")
        return

    # 1. Scan Files
    print(f"Scanning {SOURCE_DIR} for images...")
    for subdir, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith(valid_exts):
                full_path = os.path.join(subdir, file)
                rel_path = os.path.relpath(full_path, SOURCE_DIR)
                tasks.append((full_path, rel_path))

    if not tasks:
        gh_log("No images found to process.", "warning")
        gh_log("", "endgroup")
        return

    print(f"Found {len(tasks)} images. Using {os.cpu_count()} CPU cores.")
    gh_log("", "endgroup")  # End the setup group

    # 2. Execute Tasks
    gh_log(f"Processing {len(tasks)} Images...", "group")

    success_count = 0
    error_count = 0

    with ProcessPoolExecutor() as executor:
        future_to_image = {
            executor.submit(process_image_suite, task): task for task in tasks
        }

        for i, future in enumerate(as_completed(future_to_image)):
            result = future.result()

            if result["status"] == "success":
                success_count += 1
                # Log only every 10th file to prevent GitHub Actions log clutter
                if success_count % 10 == 0:
                    print(
                        f"[{i+1}/{len(tasks)}] ✅ Processed: {result['file']}",
                        flush=True,
                    )

            else:
                error_count += 1
                # Always log errors with the special error syntax
                gh_log(f"Failed: {result['file']} -> {result['msg']}", "error")

    gh_log("", "endgroup")

    # 3. Final Summary
    duration = time.time() - start_time
    gh_log("📊 Pipeline Summary", "group")
    print(f"Total Time: {duration:.2f} seconds")
    print(f"Total Images: {len(tasks)}")
    print(f"✅ Success:   {success_count}")

    if error_count > 0:
        print(f"❌ Failed:    {error_count}")
        gh_log("Some images failed to process.", "warning")
    else:
        print("❌ Failed:    0")
        print("✨ All tasks completed successfully.")

    gh_log("", "endgroup")


if __name__ == "__main__":
    run_pipeline()
