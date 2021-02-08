# Main python file

import pandas as pd
from scraping import *

SKYTRAX_URLS = {
    "Air France": "https://www.airlinequality.com/airline-reviews/air-france/",
    "Delta": "https://www.airlinequality.com/airline-reviews/delta-air-lines",
    "American Airlines": "https://www.airlinequality.com/airline-reviews/american-airlines",
    "Emirates": "https://www.airlinequality.com/airline-reviews/emirates",
    "Lufthansa": "https://www.airlinequality.com/airline-reviews/lufthansa",
    "British Airways": "https://www.airlinequality.com/airline-reviews/british-airways"
}

if __name__ == "__main__":
    data = pd.DataFrame([])
    for airline in SKYTRAX_URLS.keys():
        print(f"\n> Scraping {airline} reviews on Skytrax")
        scraper = SkytraxScraper(SKYTRAX_URLS.get(airline))
        reviews = scraper.scrape(n_pages=1)
        reviews["airline"] = airline
        data = pd.concat([data, reviews], axis=0, ignore_index=True)
    data.to_csv("data/skytrax_reviews.csv", index=False, sep="|")