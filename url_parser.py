from time import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tldextract

from datumbox_wrapper import DatumBox

from databases.database_handler import Database


class UrlParser:
    def __init__(self, url):
        self.url = url
        self.html_code = self.get_quick_html()
        self.soup = BeautifulSoup(self.html_code, 'lxml')

    def render_page(self):
        """
        Parses the web page specifies as URL in the class. It supports Javascript.
        Returns html code of the web page.
        """
        start = time()
        try:
            print("Rendering page with Selenium...")
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(self.url)
        except Exception:
            print("Can't access this website: %s" % self.url)
            raise Exception("Error while visiting the page.")

        print("Request time: %.2f s" % (time() - start))

        html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')

        return html

    def get_quick_html(self):
        print("Requesting HTML web page with requests...")
        start = time()
        html = requests.get(self.url)
        print("Request time: %.2f s" % (time() - start))

        return html.text

    def get_info(self):
        """
        Returns text containing information about the type of the web page analyzed.
        """
        text_response = "The title of this page is %s.\n" % self.soup.title.string
        print("Extracting text...")
        start = time()

        datumbox = DatumBox(api_key="3670edf305888ab66dc6d9756d0f8498")
        # Extract text from HTML code.
        text = datumbox.text_extract(text=self.html_code)
        print(f"TEXT:  {text}")

        # Get topic from text extracted.
        topic = datumbox.topic_classification(text=text)
        print(f"TOPIC: {topic}")
        text_response += f"The topic of this web page is {topic}."

        # Detect language.
        language = datumbox.detect_language(text=text)
        print(f"LANGUAGE: {language}")
        text_response += f"The language of this web page is {language}."

        print("Extraction time: %.2f s" % (time() - start))

        return text_response

    def get_article(self, paragraph):
        """
        Returns the text contained in the paragraph indicated in the request.
        """
        # Find article div.
        article_div = self.soup.find_all(name="div", attrs={'class': 'news__content'})[0]
        # If paragraph is available, read it.
        div_paragraphs = article_div.find_all('p')
        string = "%s\n %d paragraph(s) left." % (div_paragraphs[paragraph].text, len(div_paragraphs) - paragraph)
        return string

    def get_section(self, idx_article):
        """
        Returns a tuple (text, url) corresponding to the next article preview to be visualized.
        """
        articles = self.soup.find_all(name="article")
        text_response = "Article number %s/%d \n" % (str(idx_article + 1), len(articles))
        text_response += articles[idx_article].find(name="h2").text
        link = articles[idx_article].find(name='a').attrs["href"]
        print(text_response)
        return text_response, link

    def get_menu(self):
        """
        Analyze the scraped pages from the url's domain, then returns the 10 most frequent links.
        Returns a list of tuples (text, url) corresponding to the anchors present in the menu.
        """
        extracted_domain = tldextract.extract(self.url)
        domain = "{}.{}".format(extracted_domain.domain, extracted_domain.suffix)
        menu = Database().analyze_scraping(domain)
        return menu

    def go_to_section(self, name=None, number=None):
        """
        Given the name of one of the menu's entries, returns its URL.
        """
        # Get menu.
        menu = self.get_menu()
        menu_strings = [tup[0] for tup in menu]
        menu_anchors = [tup[1] for tup in menu]

        # Check if the parameter is the name of the section or the index.
        if name is not None:
            # Put all the strings to lowercase.
            menu_strings = [string.lower() for string in menu_strings]
            # Return index of string, if present. Otherwise, IndexError.
            index = menu_strings.index(name.lower())
        else:
            index = number

        return menu_anchors[index]
