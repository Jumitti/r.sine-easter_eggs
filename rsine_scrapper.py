import concurrent.futures
import json
import os
import random
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_english_word_list():
    url = "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2006/04/1-10000"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            word_elements = soup.find_all("a", title=True)
            words = [re.sub(r'\([^)]*\)', '', element.get("title")).strip() for element in word_elements]
            return words
        else:
            print(f"Request error : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error : {e}")
    return []


def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error : {e}")
    return None


def process_word(word):
    base_url = "https://r.sine.com/"
    url = f"{base_url}{word}"

    clean_word = re.sub(r'\([^)]*\)', '', word).strip()

    content1 = get_page_content(url)

    if content1 == '':
        random_pictures.append(clean_word)
    elif content1 in unique_picture:
        unique_picture[content1].append(clean_word)
    else:
        content2 = get_page_content(url)

        if content1 == content2:
            unique_picture[content1] = unique_picture.get(content1, []) + [clean_word]
        else:
            random_pictures.append(clean_word)


while True:
    word_list = []
    unique_picture = {}
    unique_picture_for_one_word = []
    random_pictures = []

    num_threads = os.cpu_count()
    use_threads = num_threads - 2
    print(f"{use_threads} threads used for the script.")

    list_of_words = input("Use Wikipedia (1) or words_dictionary.json (2) ? ")

    if list_of_words == '1':
        print("Wikipedia selected")
        number_of_words = input("All (a) or a number (type a number between 1-10000)")
        if number_of_words == "a":
            word_list = get_english_word_list()
        elif 1 <= int(number_of_words) <= 10000:
            word_list = random.sample(get_english_word_list(), int(number_of_words))
        else:
            print('Wrong input. Choose All (a) or a number between 1-10000)')

    elif list_of_words == '2':
        print("words_dictionary.json selected")
        number_of_words = input("All (a) or a number (type a number between 1-370101)")

        with open('words_dictionary.json', 'r') as file:
            data = json.load(file)

        if number_of_words == "a":
            word_list = list(data.keys())
        elif 1 <= int(number_of_words) <= 370101:
            word_list = random.sample(list(data.keys()), int(number_of_words))
        else:
            print('Wrong input. Choose All (a) or a number between 1-370101)')

    else:
        print("Error. Please use 1 for Wikipedia and 2 for words_dictionary.json")

    with concurrent.futures.ThreadPoolExecutor(max_workers=use_threads) as executor:
        with tqdm(total=len(word_list), desc="Running", unit="word", mininterval=0.1) as pbar:
            futures = {executor.submit(process_word, word): word for word in word_list}

            for future in concurrent.futures.as_completed(futures):
                pbar.update(1)

    if unique_picture or random_pictures:
        if unique_picture:
            with open("output/unique_pictures.txt", "w") as file:
                print("Create unique_pictures.txt")
                for content, words in unique_picture.items():
                    if len(words) == 1:
                        unique_picture_for_one_word.append(words[0])
                        file.write(f"{words[0]}\n")

            with open("output/same_picture.txt", "w") as file:
                print("Create same_picture.txt")
                for content, words in unique_picture.items():
                    if len(words) > 1:
                        for word in words:
                            file.write(f"{word}\n")

        if random_pictures:
            with open("output/random_pictures.txt", "w") as file:
                print("Create random_pictures.txt")
                for word in random_pictures:
                    file.write(f"{word}\n")

        break
