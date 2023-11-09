import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import random
import re


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
            print(f"Erreur de requête : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite : {e}")
    return []


def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite : {e}")
    return None


word_list = get_english_word_list()
random_word_list = random.sample(word_list, 50)

valid_content_to_words = {}
unique_valid_content_words = []
invalid_content_words = []

for word in tqdm(random_word_list, "Running"):
    base_url = "https://r.sine.com/"
    url1 = f"{base_url}{word}"

    clean_word = re.sub(r'\([^)]*\)', '', word).strip()

    content1 = get_page_content(url1)

    if content1 == '':
        invalid_content_words.append(clean_word)
    elif content1 in valid_content_to_words:
        valid_content_to_words[content1].append(clean_word)
    else:
        url2 = f"{base_url}{clean_word}"
        content2 = get_page_content(url2)

        if content1 == content2:
            valid_content_to_words[content1] = valid_content_to_words.get(content1, []) + [clean_word]
        else:
            invalid_content_words.append(clean_word)

with open("tiny_scrap/unique_pictures.txt", "w") as file:
    for content, words in valid_content_to_words.items():
        if len(words) == 1:  # Mots avec un contenu unique
            unique_valid_content_words.append(words[0])
            file.write(f"{words[0]}\n")

with open("tiny_scrap/same_picture.txt", "w") as file:
    for content, words in valid_content_to_words.items():
        if len(words) > 1:
            for word in words:
                file.write(f"{word}\n")

with open("tiny_scrap/random_pictures.txt", "w") as file:
    for word in invalid_content_words:
        file.write(f"{word}\n")
