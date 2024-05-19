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


def process_word(word):
    url_word = word.replace(' ', '%20')
    command = f'curl -o "{os.path.join(output_path, word + ".jpg")}" https://r.sine.com/{url_word}'
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    with open("output_v4/data.txt", 'r') as file:
        word_list = file.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=use_threads) as executor:
        with tqdm(total=len(word_list), desc="Running", unit="word", mininterval=0.1) as pbar:
            futures = [executor.submit(process_word, word) for word in word_list]

            for future in concurrent.futures.as_completed(futures):
                future.result()
                pbar.update(1)

