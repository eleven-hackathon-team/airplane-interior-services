import pandas as pd
import numpy as np
from selenium import webdriver



class SkytraxScraper():
    """A class to scrape www.airlinequality.com 
    """
    
    def __init__(self, url):
        """
        Parameters
        ----------
        url : string
            The URL of the website to scrape.
        """
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.data = pd.DataFrame()
      
    
    def get_reviews(self):
        self.current_reviews = self.driver.find_elements_by_xpath("//article[@itemprop='review']")
    
    
    @staticmethod
    def extract_content(review):
        """Extracts the main information from the review.

        Parameters
        ----------
        review : selenium.webdriver.remote.webelement.WebElement
            The review object to extract information of.

        Returns
        -------
        list
            date of the review, content of the review and rating associated.
        """
        date = review.find_element_by_xpath(".//time").get_attribute("datetime")
        title = review.find_element_by_xpath(".//h2[@class='text_header']").text.replace('"', "")
        content = review.find_element_by_xpath(".//div[@class='text_content ']").text.replace("✅ Trip Verified |", "")
        comment = ".".join([title, content])
        rating = review.find_element_by_xpath(".//span[@itemprop='ratingValue']").text
        
        return [date, comment, rating]
        
        
    def scrape_current_page(self):
        """Extracts information from all reviews on the current page.
        """
        self.get_reviews()
        for review in self.current_reviews:
            content = self.extract_content(review)
            self.data = self.data.append([content])
        
        
    def go_to_next_page(self):
            self.driver.find_element_by_partial_link_text(">>").click()
    
    
    def scrape(self, n_pages=np.inf):
        """Performs the whole scraping process.

        Parameters
        ----------
        n_pages : integer, optional
            The number of pages to scrape (if any), by default np.inf

        Returns
        -------
        pandas.DataFrame
            Information extracted from the reviews in the pages scraped.
        """
        current_page_no = 1
        while current_page_no <= n_pages:
            print(f"Scraping page no {current_page_no}")
            self.scrape_current_page()
            try:
                self.go_to_next_page()
            except:
                print("Last page reached.")
                break
            current_page_no += 1
        self.driver.close()
        self.data.columns = ["date", "comment", "rating"]
        self.data.reset_index(inplace=True, drop=True)
        
        return self.data