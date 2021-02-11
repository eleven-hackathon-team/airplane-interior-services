# Main python file

import pandas as pd
from selenium import webdriver
from scraping import *
from preprocessing import *
from model import BERTopicModel, VaderModel

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

    # Scraping
    print(">> Scraping")
    driver = webdriver.Chrome()

    # Scraping Skytrax 
    data_skytrax = pd.DataFrame([])
    for airline in SKYTRAX_URLS.keys():
        print(f"\n> Scraping {airline} reviews on Skytrax")
        scraper = SkytraxScraper(driver=driver, url=SKYTRAX_URLS.get(airline))
        reviews = scraper.scrape()
        reviews["airline"] = airline
        data_skytrax = pd.concat([data_skytrax, reviews], axis=0, ignore_index=True)
    data_skytrax.to_csv("data/skytrax_reviews.csv", index=False, sep="|")

    # Scraping TripAdvisor
    data_tripadvisor = pd.DataFrame([])
    for airline in TRIPADVISOR_URLS.keys():
        print(f"\n> Scraping {airline} reviews on TripAdvisor")
        scraper = TripAdvisorScraper(driver=driver, url=TRIPADVISOR_URLS.get(airline))
        reviews = scraper.scrape(n_pages=2000)
        reviews["airline"] = airline
        data_tripadvisor = pd.concat([data_tripadvisor, reviews], axis=0, ignore_index=True)
    data_tripadvisor.to_csv("data/tripadvisor_reviews.csv", index=False, sep="|")  
    driver.close()  


    # Preprocessing
    print("\n\n>> Preprocessing")
    data = Preprocessor().preprocess(path_data="data/")


    # Topic Modelling
    print("\n\n>> Topic Modelling")
    tm_model = BERTopicModel()
    clusters = tm_model.cluster_reviews(data.comment_lemmatized.values, n_topics_max=50)
    tm_model.save_model(path_save="model/")
    topics = tm_model.get_topics_description()
    data["topic_idx"] = pd.Series(clusters)
    topics.to_csv("data/topics.csv", index=False, sep=";")

    # Sentiment Analysis
    print("\n\n>> Sentiment Analysis")
    sa_model = VaderModel()
    data["polarity_score"] = data.comment.apply(lambda comment: sa_model.predict(comment))

    data[["comment", "topic_idx", "polarity_score"]].to_csv("data/output.csv", index=False, sep="|")

