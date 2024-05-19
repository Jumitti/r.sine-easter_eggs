import concurrent.futures
import json
import os
import random
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error : {e}")
    return None


def process_word(word):
    url_word = word.replace(' ', '%20')
    base_url = "https://r.sine.com/"

    url = f"{base_url}{url_word}"

    content = get_page_content(url)

    if content == '':
        random_pictures.append(word)
    elif content in unique_picture:
        unique_picture[content].append(word)
    else:
        content_2 = get_page_content(url)

        if content == content_2:
            unique_picture[content] = unique_picture.get(content, []) + [word]
        else:
            random_pictures.append(word)


unique_picture = {}
unique_picture_for_one_word = []
random_pictures = []

num_threads = os.cpu_count()
use_threads = num_threads
print(f"{use_threads} threads used for the script.")

with open("output_v4/data.txt", 'r') as file:
    word_list = file.read().splitlines()

with concurrent.futures.ThreadPoolExecutor(max_workers=use_threads) as executor:
    with tqdm(total=len(word_list), desc="Running", unit="word", mininterval=0.24) as pbar:
        futures = {executor.submit(process_word, word): word for word in word_list}

        for future in concurrent.futures.as_completed(futures):
            pbar.update(1)

if unique_picture or random_pictures:
    if unique_picture:
        with open("FDR/FDR_unique_pictures.txt", "w") as file:
            print("Create FDR_unique_pictures.txt")
            for content, words in unique_picture.items():
                if len(words) == 1:
                    unique_picture_for_one_word.append(words[0])
                    file.write(f"{words[0]}\n")

        with open("FDR/FDR_same_picture.txt", "w") as file:
            print("Create FDR_same_picture.txt")
            for content, words in unique_picture.items():
                if len(words) > 1:
                    for word in words:
                        file.write(f"{word}\n")

    if random_pictures:
        with open("FDR/FDR_random_pictures.txt", "w") as file:
            print("Create FDR_random_pictures.txt")
            for word in random_pictures:
                file.write(f"{word}\n")
