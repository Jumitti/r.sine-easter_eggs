import csv
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def scrape_page(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            print(soup)
            images = soup.find_all("img")
            results = []

            for img in images:
                src = img.get("src")
                if src:
                    filename, file_extension = src.split("/")[-1].rsplit(".", 1)

                    if not check_if_exists(filename):
                        page_link = soup.find("p").text
                        results.append([filename, file_extension, page_link])

            if results:
                with open('output_v4/data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerows(results)

            return results
        else:
            print("Request failed :", response.status_code)
            return []
    except Exception as e:
        print(f"Error: {e}, {soup}")
        return []


def check_if_exists(filename):
    with open('output_v4/data.csv', mode='r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if filename in row:
                return True
    return False


def update_progress(results):
    pbar.update(len(results))


url = "https://r.sine.com/index?html=true"
print("Scraping started...")
pbar = tqdm()

while True:
    results = scrape_page(url)
    update_progress(results)
