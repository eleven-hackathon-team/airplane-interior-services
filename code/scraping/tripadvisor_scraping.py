import pandas as pd
import numpy as np
import time
from selenium import webdriver



class TripAdvisorScraper():
    """A class to scrape www.tripadvisor.com 
    """
    
    def __init__(self, driver, url):
        """
        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver
            The webdriver object to use in order to do the scraping.
        url : string
            The URL of the website to scrape.
        """
        self.driver = driver
        self.driver.get(url)
        # Accepting cookies if the banner shows up
        try:
            self.driver.find_element_by_xpath("//button[@id='_evidon-accept-button']").click()
        except:
            pass
        self.data = pd.DataFrame()
      
    
    def _get_reviews(self):
        self.current_reviews = self.driver.find_elements_by_xpath("//div[@class='oETBfkHU']")
    

    def _extract_content(self, review):
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
        # Click on "Read more" button if comment is not expanded
        try:
            review.find_element_by_xpath(".//div[3]/div[1]/div[2]").click()
        except:
            pass
        # Basic information (date, content and rating)
        date = review.find_element_by_xpath(".//div[3]/span").text.split(": ")[-1]
        title = review.find_element_by_xpath(".//div[2]/a/span").text
        content = review.find_element_by_xpath(".//div[3]/div[1]/div[1]").text
        comment = ". ".join([title, content])
        rating = review.find_element_by_xpath(".//div[1]/div[1]/span").get_attribute("class").split("_")[-1]
        review_data = [date, comment, rating]
        
        return review_data
        
        
    def _scrape_current_page(self):
        """Extracts information from all reviews on the current page.
        """
        self._get_reviews()
        for review in self.current_reviews:
            try:
                content = self._extract_content(review)
                self.data = self.data.append([content])
            except:
                pass
        
        
    def _go_to_next_page(self):
            self.driver.find_element_by_partial_link_text("Next").click()
    
    
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
            self._scrape_current_page()
            try:
                self._go_to_next_page()
                time.sleep(2)
            except:
                print("Last page reached.")
                break
            current_page_no += 1
        self.data.columns = ["date", "comment", "rating"]
        self.data.reset_index(inplace=True, drop=True)
        
        return self.data
