import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup


def main():
    # Set up chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    # Grab pre-existing list of artists
    with open('list_of_artists.json', 'r') as file:
        artist_set = set(json.loads(file.read())['data'])

    driver.get("https://maudica.com/")
    print("Waiting for page to load")
    sleep(2)
    print("Finding useful button elements...")
    next_button = driver.find_element(By.XPATH, value='/html/body/div[1]/div/main/div/div[1]/div[2]/button')

    # Set filters
    sort_and_filter = driver.find_element(By.XPATH, value='/html/body/div[1]/div/main/div/div[2]/div/div[1]/div[1]/button[1]')
    sort_and_filter.click()
    sleep(0.25)
    downloads_button = driver.find_element(By.XPATH, value='/html/body/div[1]/div/main/div/div[2]/div/div[1]/div[2]/div[3]/div[2]/button[3]')
    downloads_button.click()
    sleep(2) # Load in new songs

    # Get each page
    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")

        songs = soup.find_all('a', class_='map panel svelte-rclfgg')
        for index, song in enumerate(songs, start=1):
            spans = song.find_all('span')
            song_name = spans[0].text
            artist = spans[1].text

            if artist in artist_set:
                print(f">Grabbing '{song_name}' by '{artist}'")
                # Click the song and download it
                driver.find_element(By.XPATH, value=f'//*[@id="app"]/div/main/div/div[1]/a[{index}]/div[2]/div[3]/div[4]/a').click()
                sleep(2)
        #input("Press enter for next page >_")
        next_button.click()
        sleep(3) # Load in new songs


if __name__ == "__main__":
    main()
