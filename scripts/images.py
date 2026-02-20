import os
import logging
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
SOURCE_DIR = "./images"
WEB_LIB_DIR = "website/src/lib/images"
WEBP_DIR = "./images_default"
JPEG_DIR = "./images_legacy"

# Simplified logging: only print to console in real-time
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",  # Clean output without timestamps for readability
    handlers=[logging.StreamHandler()],
)


def process_image_suite(paths):
    """Processes a single image and returns a status string."""
    input_path, relative_path = paths
    filename = os.path.basename(input_path)

    web_lib_path = os.path.join(WEB_LIB_DIR, relative_path)
    webp_path = os.path.join(WEBP_DIR, os.path.splitext(relative_path)[0] + ".webp")
    jpeg_path = os.path.join(JPEG_DIR, os.path.splitext(relative_path)[0] + ".jpg")

    for p in [web_lib_path, webp_path, jpeg_path]:
        os.makedirs(os.path.dirname(p), exist_ok=True)

    try:
        # 1. Copy Original
        shutil.copy2(input_path, web_lib_path)

        # 2. WebP Conversion
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

        # 3. JPEG B&W Conversion
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

        return f"SUCCESS: {filename}"

    except Exception as e:
        return f"CRITICAL ERROR on {filename}: {str(e)}"


def run_pipeline():
    valid_exts = (".jpg", ".jpeg", ".png", ".tiff", ".webp")
    tasks = []
    shutil.rmtree(WEB_LIB_DIR)

    if not os.path.exists(SOURCE_DIR):
        print(f"Source directory {SOURCE_DIR} not found.")
        return

    print(f"--- Pipeline Started at {datetime.now().strftime('%H:%M:%S')} ---")

    for subdir, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith(valid_exts):
                full_path = os.path.join(subdir, file)
                rel_path = os.path.relpath(full_path, SOURCE_DIR)
                tasks.append((full_path, rel_path))

    if not tasks:
        print("No images found to process.")
        return

    print(f"Processing {len(tasks)} images... (Logging in real-time)\n")

    # Use as_completed to yield results as soon as each process finishes
    with ProcessPoolExecutor() as executor:
        future_to_image = {
            executor.submit(process_image_suite, task): task for task in tasks
        }

        for future in as_completed(future_to_image):
            result = future.result()
            logging.info(result)  # This prints immediately when the file is done

    print(f"\n--- All Tasks Complete at {datetime.now().strftime('%H:%M:%S')} ---")


if __name__ == "__main__":
    run_pipeline()
