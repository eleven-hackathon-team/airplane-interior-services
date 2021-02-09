import pandas as pd
import numpy as np
from selenium import webdriver



class SkytraxScraper():
    """A class to scrape www.airlinequality.com 
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
        self.data = pd.DataFrame()
        self.additional_fields = [
            "aircraft", 
            "cabin_flown", 
            "seat_comfort"
        ]
        self.rating_fields = [
            "cabin_staff_service", 
            "food_and_beverage", 
            "inflight_entertainment", 
            "ground_service",
            "wifi_and_connectivity", 
            "value_for_money"
        ]
      
    
    def get_reviews(self):
        self.current_reviews = self.driver.find_elements_by_xpath("//article[@itemprop='review']")
    

    def extract_content(self, review):
        """Extracts the main information from the review.

        Parameters
        ----------
        review : selenium.webdriver.remote.webelement.WebElement
            The review object to extract information of.

        Returns
        -------
        list
            date of the review, content of the review and rating associated, and additional fields specified.
        """
        # Basic information (date, content and rating)
        date = review.find_element_by_xpath(".//time").get_attribute("datetime")
        title = review.find_element_by_xpath(".//h2[@class='text_header']").text.replace('"', "")
        content = review.find_element_by_xpath(".//div[@class='text_content ']").text.replace("✅ Trip Verified |", "")
        comment = ".".join([title, content])
        rating = review.find_element_by_xpath(".//span[@itemprop='ratingValue']").text
        review_data = [date, comment, rating]
        
        # Additional fields 
        for field in self.additional_fields:
            field_header = review.find_elements_by_xpath(f".//td[@class='review-rating-header {field} ']")
            if len(field_header) > 0: # if the field has not been filled by the customer, len(field_header)=0
                field_content = field_header[0].find_element_by_xpath("./../td[2]").text
            else:
                field_content = ""
            review_data.append(field_content)
        
        # Rating fields
        for field in self.rating_fields:
            field_header = review.find_elements_by_xpath(f".//td[@class='review-rating-header {field}']")
            if len(field_header) > 0:
                # the text from the last filled star indicates the rating
                field_rating = field_header[0].find_elements_by_xpath("./../td[2]/span[@class='star fill']")[-1].text 
            else:
                field_rating = ""
            review_data.append(field_rating)
        
        return review_data
        
        
    def scrape_current_page(self):
        """Extracts information from all reviews on the current page.
        """
        self.get_reviews()
        for review in self.current_reviews:
            try:
                content = self.extract_content(review)
                self.data = self.data.append([content])
            except:
                pass
        
        
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
        self.data.columns = ["date", "comment", "rating"] + self.additional_fields + self.rating_fields
        self.data.reset_index(inplace=True, drop=True)
        
        return self.data