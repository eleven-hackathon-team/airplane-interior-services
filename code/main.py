# Main python file

import pandas as pd
from selenium import webdriver
from scraping import *
from preprocessing import *
from model import *

SKYTRAX_URLS = {
    "Air France": "https://www.airlinequality.com/airline-reviews/air-france/",
    "Delta": "https://www.airlinequality.com/airline-reviews/delta-air-lines",
    "American Airlines": "https://www.airlinequality.com/airline-reviews/american-airlines",
    "Emirates": "https://www.airlinequality.com/airline-reviews/emirates",
    "Lufthansa": "https://www.airlinequality.com/airline-reviews/lufthansa",
    "British Airways": "https://www.airlinequality.com/airline-reviews/british-airways"
}

TRIPADVISOR_URLS = {
    "Air France": "https://www.tripadvisor.com/Airline_Review-d8729003-Reviews-Air-France.html#REVIEWS",
    "Delta": "https://www.tripadvisor.com/Airline_Review-d8729060-Reviews-Delta-Air-Lines.html#REVIEWS",
    "American Airlines": "https://www.tripadvisor.com/Airline_Review-d8729020-Reviews-American-Airlines",
    "Emirates": "https://www.tripadvisor.com/Airline_Review-d8729069-Reviews-Emirates",
    "Lufthansa": "https://www.tripadvisor.com/Airline_Review-d8729113-Reviews-Lufthansa",
    "British Airways": "https://www.tripadvisor.com/Airline_Review-d8729039-Reviews-British-Airways"
}

if __name__ == "__main__":

    # # Scraping
    # driver = webdriver.Chrome()
    # # Scraping Skytrax 
    # data_skytrax = pd.DataFrame([])
    # for airline in SKYTRAX_URLS.keys():
    #     print(f"\n> Scraping {airline} reviews on Skytrax")
    #     scraper = SkytraxScraper(driver=driver, url=SKYTRAX_URLS.get(airline))
    #     reviews = scraper.scrape()
    #     reviews["airline"] = airline
    #     data_skytrax = pd.concat([data_skytrax, reviews], axis=0, ignore_index=True)
    # data_skytrax.to_csv("data/skytrax_reviews.csv", index=False, sep="|")
    # # Scraping TripAdvisor
    # data_tripadvisor = pd.DataFrame([])
    # for airline in TRIPADVISOR_URLS.keys():
    #     print(f"\n> Scraping {airline} reviews on TripAdvisor")
    #     scraper = TripAdvisorScraper(driver=driver, url=TRIPADVISOR_URLS.get(airline))
    #     reviews = scraper.scrape(n_pages=2000)
    #     reviews["airline"] = airline
    #     data_tripadvisor = pd.concat([data_tripadvisor, reviews], axis=0, ignore_index=True)
    # data_tripadvisor.to_csv("data/tripadvisor_reviews.csv", index=False, sep="|")  
    # driver.close()  


    # Preprocessing
    data = Preprocessor().preprocess(path_data="data/")
    print(data.shape)

    # Modelling
    sa_model = VaderModel()
    print(sa_model.predict(data.comment.values[0]))
