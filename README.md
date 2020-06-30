
# News Analyzer module

Basic news analyzer. For now, only operates to some Ecuadorian media press outlets. 
You may want to fill up some real news examples to files within `./data/` folder, otherwise the provider analysis won't work properly (It's possible to obtain such data through the Ruby component).

## Initial setup

Install all project dependencies:

`pip3 install -r requirements.txt`

## Run server

`FLASK_APP=main.py flask run`

## Using it

### Analyzing single news

`curl https://localhost:5000/analyze-news\?url\="<url>"`

### Analyzing news set

`curl https://localhost:5000/analyze-provider/<provider>`