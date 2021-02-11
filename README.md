# Airplane Interior Services

Repository for the Airplane Interior Services project of the 2021 Eleven Strategy x DSBA hackathon.

### Environment Setup
```
conda create -n ais python=3.8
conda activate ais
pip install -r requirements.txt
```

### How to run the code 
After setting the environment up, run the main.py file to perform the scraping, topic modelling and sentiment analysis. The postprocessing.ipynb notebook is used to do analyze in more details the results.


### Structure
```
.
├── code/
|   ├── model/
|   |   ├── sentiment_analysis/         <- models for sentiment analysis (vader, textblob and flair)
|   |   |   ├── flair_model.py
|   |   |   ├── textblob.py
|   |   |   └── vader.py
|   |   ├── topic_modelling/            <- models for topic modelling (BERT-based and LDA)
|   |   |   ├── bertopic.py
|   |   |   └── LDA.ipynb
|   |   └── __init__.py
|   ├── preprocessing/          
|   |   ├── __init__.py
|   |   └── preprocessing.py
|   ├── scraping/
|   |   ├── __init__.py
|   |   ├── skytrax_scraping.py
|   |   └── tripadvisor_scraping.py     
|   ├── main.py
|   └── postprocessing.ipynb
├── data/                               
├── docs/
├── chromedriver.exe
├── README.md
└── requirements.txt
```
