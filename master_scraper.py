import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from unidecode import unidecode


# pip install lxml beforehand to run
# pip install beautifulsoup4 beforehand to run


def safe_post(url, payload, headers, retries=3):
    for i in range(retries):
        try:
            return requests.post(url, json=payload, headers=headers, timeout=20)  # noqa: E501
        except requests.exceptions.RequestException as e:
            print(f"Retry {i+1} failed: {e}")
            time.sleep(2 ** i)
    raise Exception("Failed after retries")


def scraper_nine_billion(url: str) -> pd.DataFrame:
    '''
    Scrapes given URL into dataframe.
    '''
    response = requests.get(url)
    html = response.text

    # beautifulsoup parsing
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table')

    # [0] takes first table from page
    try:
        tables = pd.read_html(url)
    except ValueError as e:
        print(url)
        print(e)
        return None

    df = tables[0]

    # pd.read_html(url)[0] makes a random irrelevant column.
    # Line of code drops that column.
    df = df.drop(columns=['Unnamed: 7', 'WIND'], errors='ignore')

    # pd.read_html(url)[0] doesn't name Country column correctly.
    df = df.rename(columns={'Unnamed: 5': 'Country'})

    athlete_links = []
    athlete_ids = []

    for link in table.find_all('a', href=True):
        href = link['href']

        if "/athletes/" in href:
            full_url = "https://worldathletics.org" + href
            athlete_links.append(full_url)
            athlete_ids.append(full_url[-8:])

    athlete_links = list(dict.fromkeys(athlete_links))
    df = df.iloc[:len(athlete_links)].copy()
    df['athlete_id'] = athlete_ids[:len(df)]
    df["profile_url"] = athlete_links[:len(df)]

    return df


# Links we want to scrape data
men_urls2022 = [
    'https://worldathletics.org/records/toplists/sprints/100-metres/all/men/senior/2022?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229630&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/200-metres/all/men/senior/2022?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229605&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/400-metres/all/men/senior/2022?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229631&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/800-metres/all/men/senior/2022?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229501&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/1500-metres/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229502&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/one-mile/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229503&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/5000-metres/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229609&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/10000-metres/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229610&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/110-metres-hurdles/all/men/senior/2022?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229611&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/400-metres-hurdles/all/men/senior/2022?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229612&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229614&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/high-jump/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229615&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/pole-vault/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229616&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/long-jump/all/men/senior/2022?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229617&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/triple-jump/all/men/senior/2022?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229618&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/shot-put/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229619&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/discus-throw/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229620&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/hammer-throw/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229621&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/javelin-throw/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229636&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/road-running/marathon/all/men/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229634&ageCategory=senior',  # noqa: E501
]

men_urls2023 = [
    'https://worldathletics.org/records/toplists/sprints/100-metres/all/men/senior/2023?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229630&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/200-metres/all/men/senior/2023?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229605&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/400-metres/all/men/senior/2023?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229631&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/800-metres/all/men/senior/2023?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229501&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/1500-metres/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229502&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/one-mile/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229503&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/5000-metres/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229609&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/10000-metres/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229610&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/110-metres-hurdles/all/men/senior/2023?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229611&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/400-metres-hurdles/all/men/senior/2023?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229612&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229614&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/high-jump/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229615&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/pole-vault/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229616&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/long-jump/all/men/senior/2023?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229617&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/triple-jump/all/men/senior/2023?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229618&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/shot-put/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229619&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/discus-throw/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229620&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/hammer-throw/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229621&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/javelin-throw/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229636&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/road-running/marathon/all/men/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229634&ageCategory=senior',  # noqa: E501
]

men_urls2024 = [
    'https://worldathletics.org/records/toplists/sprints/100-metres/all/men/senior/2024?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229630&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/200-metres/all/men/senior/2024?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229605&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/400-metres/all/men/senior/2024?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229631&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/800-metres/all/men/senior/2024?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229501&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/1500-metres/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229502&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/one-mile/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229503&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/5000-metres/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229609&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/10000-metres/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229610&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/110-metres-hurdles/all/men/senior/2024?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229611&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/400-metres-hurdles/all/men/senior/2024?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229612&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229614&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/high-jump/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229615&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/pole-vault/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229616&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/long-jump/all/men/senior/2024?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229617&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/triple-jump/all/men/senior/2024?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229618&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/shot-put/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229619&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/discus-throw/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229620&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/hammer-throw/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229621&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/javelin-throw/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229636&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/road-running/marathon/all/men/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229634&ageCategory=senior',  # noqa: E501
]


men_urls2025 = [
    'https://worldathletics.org/records/toplists/sprints/100-metres/all/men/senior/2025?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229630&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/200-metres/all/men/senior/2025?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229605&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/400-metres/all/men/senior/2025?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229631&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/800-metres/all/men/senior/2025?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229501&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/1500-metres/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229502&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/one-mile/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229503&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/5000-metres/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229609&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/10000-metres/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229610&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/110-metres-hurdles/all/men/senior/2025?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229611&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/400-metres-hurdles/all/men/senior/2025?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229612&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229614&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/high-jump/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229615&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/pole-vault/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229616&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/long-jump/all/men/senior/2025?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229617&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/triple-jump/all/men/senior/2025?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229618&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/shot-put/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229619&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/discus-throw/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229620&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/hammer-throw/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229621&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/javelin-throw/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229636&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/road-running/marathon/all/men/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229634&ageCategory=senior',  # noqa: E501
]

men_urls2026 = [
    'https://worldathletics.org/records/toplists/sprints/100-metres/all/men/senior/2026?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229630&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/200-metres/all/men/senior/2026?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229605&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/400-metres/all/men/senior/2026?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229631&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/800-metres/all/men/senior/2026?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229501&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/1500-metres/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229502&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/one-mile/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229503&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/5000-metres/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229609&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/10000-metres/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229610&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/110-metres-hurdles/all/men/senior/2026?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229611&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/400-metres-hurdles/all/men/senior/2026?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229612&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229614&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/high-jump/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229615&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/pole-vault/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229616&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/long-jump/all/men/senior/2026?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229617&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/triple-jump/all/men/senior/2026?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229618&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/shot-put/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229619&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/discus-throw/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229620&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/hammer-throw/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229621&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/javelin-throw/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229636&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/road-running/marathon/all/men/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229634&ageCategory=senior',  # noqa: E501
]

women_urls2022 = [
    'https://worldathletics.org/records/toplists/sprints/100-metres/all/women/senior/2022?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229509&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/200-metres/all/women/senior/2022?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229510&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/400-metres/all/women/senior/2022?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229511&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/800-metres/all/women/senior/2022?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229512&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/1500-metres/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229513&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/one-mile/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229517&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/5000-metres/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229514&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/10000-metres/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229521&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/100-metres-hurdles/all/women/senior/2022?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229522&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/400-metres-hurdles/all/women/senior/2022?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229523&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229524&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/high-jump/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229526&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/pole-vault/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229527&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/long-jump/all/women/senior/2022?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229528&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/triple-jump/all/women/senior/2022?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229529&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/shot-put/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229530&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/discus-throw/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229531&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/hammer-throw/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229532&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/javelin-throw/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229533&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/road-running/marathon/all/women/senior/2022?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229534&ageCategory=senior'  # noqa: E501
]

women_urls2023 = [
    'https://worldathletics.org/records/toplists/sprints/100-metres/all/women/senior/2023?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229509&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/200-metres/all/women/senior/2023?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229510&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/400-metres/all/women/senior/2023?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229511&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/800-metres/all/women/senior/2023?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229512&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/1500-metres/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229513&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/one-mile/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229517&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/5000-metres/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229514&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/10000-metres/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229521&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/100-metres-hurdles/all/women/senior/2023?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229522&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/400-metres-hurdles/all/women/senior/2023?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229523&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229524&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/high-jump/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229526&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/pole-vault/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229527&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/long-jump/all/women/senior/2023?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229528&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/triple-jump/all/women/senior/2023?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229529&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/shot-put/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229530&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/discus-throw/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229531&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/hammer-throw/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229532&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/javelin-throw/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229533&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/road-running/marathon/all/women/senior/2023?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229534&ageCategory=senior'  # noqa: E501
]

women_urls2024 = [
    'https://worldathletics.org/records/toplists/sprints/100-metres/all/women/senior/2024?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229509&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/200-metres/all/women/senior/2024?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229510&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/400-metres/all/women/senior/2024?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229511&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/800-metres/all/women/senior/2024?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229512&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/1500-metres/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229513&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/one-mile/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229517&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/5000-metres/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229514&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/10000-metres/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229521&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/100-metres-hurdles/all/women/senior/2024?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229522&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/400-metres-hurdles/all/women/senior/2024?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229523&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229524&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/high-jump/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229526&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/pole-vault/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229527&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/long-jump/all/women/senior/2024?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229528&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/triple-jump/all/women/senior/2024?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229529&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/shot-put/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229530&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/discus-throw/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229531&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/hammer-throw/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229532&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/javelin-throw/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229533&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/road-running/marathon/all/women/senior/2024?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229534&ageCategory=senior'  # noqa: E501
]

women_urls2025 = [
    'https://worldathletics.org/records/toplists/sprints/100-metres/all/women/senior/2025?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229509&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/200-metres/all/women/senior/2025?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229510&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/400-metres/all/women/senior/2025?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229511&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/800-metres/all/women/senior/2025?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229512&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/1500-metres/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229513&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/one-mile/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229517&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/5000-metres/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229514&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/10000-metres/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229521&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/100-metres-hurdles/all/women/senior/2025?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229522&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/400-metres-hurdles/all/women/senior/2025?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229523&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229524&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/high-jump/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229526&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/pole-vault/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229527&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/long-jump/all/women/senior/2025?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229528&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/triple-jump/all/women/senior/2025?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229529&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/shot-put/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229530&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/discus-throw/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229531&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/hammer-throw/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229532&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/javelin-throw/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229533&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/road-running/marathon/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229534&ageCategory=senior'  # noqa: E501
]

women_urls2026 = [
    'https://worldathletics.org/records/toplists/sprints/100-metres/all/women/senior/2026?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229509&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/200-metres/all/women/senior/2026?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229510&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/sprints/400-metres/all/women/senior/2026?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229511&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/800-metres/all/women/senior/2026?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229512&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/1500-metres/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229513&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/one-mile/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229517&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/5000-metres/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229514&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/10000-metres/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229521&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/100-metres-hurdles/all/women/senior/2026?regionType=world&timing=electronic&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229522&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/hurdles/400-metres-hurdles/all/women/senior/2026?regionType=world&timing=electronic&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229523&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229524&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/high-jump/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229526&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/pole-vault/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229527&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/long-jump/all/women/senior/2026?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229528&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/jumps/triple-jump/all/women/senior/2026?regionType=world&windReading=regular&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229529&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/shot-put/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229530&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/discus-throw/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229531&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/hammer-throw/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229532&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/throws/javelin-throw/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229533&ageCategory=senior',  # noqa: E501
    'https://worldathletics.org/records/toplists/road-running/marathon/all/women/senior/2026?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229534&ageCategory=senior'  # noqa: E501
]

# Event corresponding to link
mens_events = [
    "Mens 100 Metres",
    "Mens 200 Metres",
    "Mens 400 Metres",
    "Mens 800 Metres",
    "Mens 1500 Metres",
    "Mens One Mile",
    "Mens 5000 Metres",
    "Mens 10,000 Metres",
    "Mens 110 Metres Hurdles",
    "Mens 400 Metres Hurdles",
    "Mens 3000 Metres Steeplechase",
    "Mens High Jump",
    "Mens Pole Vault",
    "Mens Long Jump",
    "Mens Triple Jump",
    "Mens Shot Put",
    "Mens Discus Throw",
    "Mens Hammer Throw",
    "Mens Javelin Throw",
    "Mens Marathon",
]

womens_events = [
    "Womens 100 Metres",
    "Womens 200 Metres",
    "Womens 400 Metres",
    "Womens 800 Metres",
    "Womens 1500 Metres",
    "Womens One Mile",
    "Womens 5000 Metres",
    "Womens 10,000 Metres",
    "Womens 100 Metres Hurdles",
    "Womens 400 Metres Hurdles",
    "Womens 3000 Metres Steeplechase",
    "Womens High Jump",
    "Womens Pole Vault",
    "Womens Long Jump",
    "Womens Triple Jump",
    "Womens Shot Put",
    "Womens Discus Throw",
    "Womens Hammer Throw",
    "Womens Javelin Throw",
    "Womens Marathon",
]

payload = {
    "operationName": "GetSingleCompetitorResultsDate",
    "query": """
    query GetSingleCompetitorResultsDate($id: Int, $resultsByYearOrderBy:
    String,$resultsByYear: Int) {
    getSingleCompetitorResultsDate(
    id: $id,
    resultsByYear: $resultsByYear,
    resultsByYearOrderBy: $resultsByYearOrderBy
    ) {
    resultsByDate {
        date
        competition
        venue
        discipline
        mark
        place
        resultScore
    }
    }
}
""",
    "variables": {
        "id": None,
        "resultsByYear": 2025,
        "resultsByYearOrderBy": "date"
    }
}

GRAPHQL_QUERY = payload["query"]


def get_athlete_results(athlete_id, year):

    url = "https://graphql-prod-4875.edge.aws.worldathletics.org/graphql"

    payload = {
        "operationName": "GetSingleCompetitorResultsDate",
        "query": GRAPHQL_QUERY,
        "variables": {
            "id": int(athlete_id),
            "resultsByYear": year,
            "resultsByYearOrderBy": "date"
        }
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",  # noqa: E501
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://worldathletics.org",
        "Referer": "https://worldathletics.org/",
        "Accept-Language": "en-US,en;q=0.9",
        "x-amz-user-agent": "aws-amplify/3.0.2",
        "x-api-key": "da2-jkcja3ykujbf3cz64fs7w5gl6m",
    }

    r = safe_post(url, payload, headers)

    try:
        return r.json()
    except Exception as e:
        print("FAILED JSON PARSE:", e)
        return None


def scrape_individual(person_id, name, gender: str) -> None:
    results22 = get_athlete_results(person_id, 2022)
    results23 = get_athlete_results(person_id, 2023)
    results24 = get_athlete_results(person_id, 2024)
    results25 = get_athlete_results(person_id, 2025)
    results26 = get_athlete_results(person_id, 2026)
    results_df = pd.DataFrame()
    if results22['data']['getSingleCompetitorResultsDate'] is not None:  # noqa: E501
        results_df = pd.concat([results_df, pd.DataFrame(results22['data']['getSingleCompetitorResultsDate']['resultsByDate'])], ignore_index=True)  # noqa: E501
    if results23['data']['getSingleCompetitorResultsDate'] is not None:  # noqa: E501
        results_df = pd.concat([results_df, pd.DataFrame(results23['data']['getSingleCompetitorResultsDate']['resultsByDate'])], ignore_index=True)  # noqa: E501
    if results24['data']['getSingleCompetitorResultsDate'] is not None:  # noqa: E501
        results_df = pd.concat([results_df, pd.DataFrame(results24['data']['getSingleCompetitorResultsDate']['resultsByDate'])], ignore_index=True)  # noqa: E501
    if results25['data']['getSingleCompetitorResultsDate'] is not None:  # noqa: E501
        results_df = pd.concat([results_df, pd.DataFrame(results25['data']['getSingleCompetitorResultsDate']['resultsByDate'])], ignore_index=True)  # noqa: E501
    if results26['data']['getSingleCompetitorResultsDate'] is not None:  # noqa: E501
        results_df = pd.concat([results_df, pd.DataFrame(results26['data']['getSingleCompetitorResultsDate']['resultsByDate'])], ignore_index=True)  # noqa: E501
    results_df.insert(0, 'name', name)
    results_df.insert(1, 'gender', gender)

    csv_name = 'athlete_files/' + str(person_id) + '.csv'
    results_df.to_csv(csv_name, index=False)

# Store scraped data into csvs


def scrape_all() -> None:
    """
    Scrapes all men's and women's toplists for 2024-2026 and saves
    results to event_files/ and athlete_files/ as CSVs.
    """
    collected_athletes = {}
    print("Scrape begun")

    for url, event in zip(men_urls2022, mens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2022 ' + event + '.csv'
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        # scrape_individual(person_id, name, 'Men')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2022 Men's complete")

    for url, event in zip(men_urls2023, mens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2023 ' + event + '.csv'
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        # scrape_individual(person_id, name, 'Men')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2023 Men's complete")

    for url, event in zip(men_urls2024, mens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2024 ' + event + '.csv'
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        # scrape_individual(person_id, name, 'Men')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2024 Men's complete")

    for url, event in zip(men_urls2025, mens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2025 ' + event + '.csv'
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        # scrape_individual(person_id, name, 'Men')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2025 Men's complete")

    for url, event in zip(men_urls2026, mens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2026 ' + event + '.csv'
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        # scrape_individual(person_id, name, 'Men')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2026 Men's complete")

    for url, event in zip(women_urls2022, womens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2022 ' + event + '.csv'
        # turn dataframe into csv,
        # index=False makes indexes as intended
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        # scrape_individual(person_id, name, 'Women')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2022 Women's complete")

    for url, event in zip(women_urls2023, womens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2023 ' + event + '.csv'
        # turn dataframe into csv,
        # index=False makes indexes as intended
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        # scrape_individual(person_id, name, 'Women')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2023 Women's complete")

    for url, event in zip(women_urls2024, womens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2024 ' + event + '.csv'
        # turn dataframe into csv,
        # index=False makes indexes as intended
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        # scrape_individual(person_id, name, 'Women')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2024 Women's complete")

    for url, event in zip(women_urls2025, womens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2025 ' + event + '.csv'
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        # scrape_individual(person_id, name, 'Women')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2025 Women's complete")

    for url, event in zip(women_urls2026, womens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2026 ' + event + '.csv'
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        # scrape_individual(person_id, name, 'Women')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2026 Women's complete")
    all_athletes = pd.DataFrame([collected_athletes])
    all_athletes.to_csv('athlete_files/all_athletes.csv')
    print(len(collected_athletes))


def scrape26():
    collected_athletes = {}
    print("Scrape begun")

    for url, event in zip(men_urls2026, mens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2026 ' + event + '.csv'
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        scrape_individual(person_id, name, 'Men')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2026 Men's complete")

    for url, event in zip(women_urls2026, womens_events):
        df = scraper_nine_billion(url)
        csv_name = 'event_files/2026 ' + event + '.csv'
        if df is not None:
            df.to_csv(csv_name, index=False)
            for athlete in df:
                athlete_ids = df['athlete_id']
                names = df['Competitor']
                for person_id, name in zip(athlete_ids, names):
                    if person_id in collected_athletes:
                        # we skip over to save compute power
                        pass
                    else:
                        scrape_individual(person_id, name, 'Women')
                        collected_athletes[person_id] = unidecode(name)
    print(len(collected_athletes))
    print("2026 Women's complete")
    all_athletes = pd.DataFrame([collected_athletes])
    all_athletes.to_csv('athlete_files/all_athletes.csv')
    print(len(collected_athletes))


def main():
    # scrape_all()
    scrape26()


if __name__ == '__main__':
    main()
