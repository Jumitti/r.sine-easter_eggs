import concurrent.futures
import json
import os
import random
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

num_threads = os.cpu_count()
use_threads = num_threads - 2
print(f"{use_threads} threads used for the script.")
output_file = "SC_per_picture_sorted.txt"


def get_word_list(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()


def process_word(word):
    base_url = "https://r.sine.com/"
    url = f"{base_url}{word}"

    clean_word = re.sub(r'\([^)]*\)', '', word).strip()

    content = get_page_content(url)

    if content and ("JFIF" in content or "PNG" in content or "Exif" in content or "ICC_PROFILE" in content):
        return f"{clean_word}  flag: PIC"
    if content and "GIF" in content:
        return f"{clean_word}  flag: GIF"
    else:
        return f"{clean_word}  flag: {str(content)}"


def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error : {e}")
    return None


def write_to_text(data):
    with open(output_file, "w", encoding="utf-8") as file:
        for item in data:
            file.write(f"{item}\n")
    print(f"Results written to {output_file}")


if __name__ == "__main__":
    word_list = get_word_list("special_words/compilation_unique_pictures.txt")

    result_data = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=use_threads) as executor:
        with tqdm(total=len(word_list), desc="Running", unit="word", mininterval=0.1) as pbar:
            futures = [executor.submit(process_word, word) for word in word_list]

            for future in concurrent.futures.as_completed(futures):
                result_data.append(future.result())
                pbar.update(1)

    write_to_text(result_data)
