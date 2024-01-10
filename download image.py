import subprocess
import concurrent.futures
import json
import os
import random
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

script_directory = os.path.dirname(os.path.abspath(__file__))
output_directory = 'image'
output_path = os.path.join(script_directory, output_directory)
os.makedirs(output_path, exist_ok=True)

num_threads = os.cpu_count()
use_threads = num_threads - 2
print(f"{use_threads} threads used for the script.")
output_file = "SC_per_picture_sorted.txt"


def get_word_list(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()


def process_word(word):
    command = f'curl -o "{os.path.join(output_path, word + ".png")}" https://r.sine.com/{word}'
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    word_list = get_word_list("special_words/compilation_unique_pictures.txt")

    with concurrent.futures.ThreadPoolExecutor(max_workers=use_threads) as executor:
        with tqdm(total=len(word_list), desc="Running", unit="word", mininterval=0.1) as pbar:
            futures = [executor.submit(process_word, word) for word in word_list]

            for future in concurrent.futures.as_completed(futures):
                future.result()
                pbar.update(1)

