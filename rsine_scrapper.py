import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import json
import random


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


while True:
    word_list = []
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

    valid_content_to_words = {}
    unique_valid_content_words = []
    invalid_content_words = []

    if word_list:
        for word in tqdm(word_list, "Running"):
            base_url = "https://r.sine.com/"
            url = f"{base_url}{word}"

            clean_word = re.sub(r'\([^)]*\)', '', word).strip()

            content1 = get_page_content(url)

            if content1 == '':
                invalid_content_words.append(clean_word)
            elif content1 in valid_content_to_words:
                valid_content_to_words[content1].append(clean_word)
            else:
                content2 = get_page_content(url)

                if content1 == content2:
                    valid_content_to_words[content1] = valid_content_to_words.get(content1, []) + [clean_word]
                else:
                    invalid_content_words.append(clean_word)

    if valid_content_to_words or invalid_content_words:
        if valid_content_to_words:
            with open("output/unique_pictures.txt", "w") as file:
                print("Create unique_pictures.txt")
                for content, words in valid_content_to_words.items():
                    if len(words) == 1:
                        unique_valid_content_words.append(words[0])
                        file.write(f"{words[0]}\n")

            with open("output/same_picture.txt", "w") as file:
                print("Create same_picture.txt")
                for content, words in valid_content_to_words.items():
                    if len(words) > 1:
                        for word in words:
                            file.write(f"{word}\n")

        if invalid_content_words:
            with open("output/random_pictures.txt", "w") as file:
                print("Create random_pictures.txt")
                for word in invalid_content_words:
                    file.write(f"{word}\n")

        break
