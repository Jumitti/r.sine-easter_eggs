import os
import requests
from tqdm import tqdm
from urllib.parse import quote
from pathlib import Path
from mimetypes import guess_extension
import concurrent.futures
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

output_dir = Path("image")
output_dir.mkdir(parents=True, exist_ok=True)


def get_image_extension(content_type):
    if not content_type or "image" not in content_type:
        return None
    return guess_extension(content_type.split(";")[0].strip())


def download_image(word):
    url = f"https://sine.com/{quote(word)}"
    try:
        response = requests.get(url, stream=True, timeout=10, verify=False)
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type")
            ext = get_image_extension(content_type)
            if ext:
                filename = f"{word}{ext}"
                filepath = output_dir / filename
                if filepath.exists():
                    return f"✔️ {filename} already exists, skipped."
                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return f"✅ {filename} saved"
            else:
                return f"❌ Unknown image type for {word} ({content_type})"
        else:
            return f"❌ Failed to fetch {word} (status {response.status_code})"
    except Exception as e:
        return f"❌ Error for {word}: {e}"


with open("special_words/compilation_unique_pictures.txt", "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]

num_threads = max(os.cpu_count() - 2, 1)
print(f"{num_threads} threads used for downloading {len(words)} images...\n")

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    with tqdm(total=len(words), desc="Downloading", unit="img", mininterval=0.1) as pbar:
        futures = {executor.submit(download_image, word): word for word in words}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)
            pbar.update(1)
