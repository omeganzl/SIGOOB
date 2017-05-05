import bs4
import requests


def get_bbc_headlines():

    res = requests.get('http://www.bbc.com')
    res.raise_for_status()
    bbc_soup = bs4.BeautifulSoup(res.text)

    headlines = bbc_soup.select('.media__link')
    headline_text = [headline.getText().strip() for headline in headlines]
    return headline_text

