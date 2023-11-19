[![Unit Test](https://github.com/thanidacwn/veggie-hub/actions/workflows/python-publish.yml/badge.svg)](https://github.com/thanidacwn/veggie-hub/actions/workflows/python-publish.yml)

# VeggieHub
VeggieHub is a web app designed to assist users to make informed choices about their vegetarian dining. It allows users to review and rate various vegetarian restaurants, creating a platform where they can share their dining experiences, preferences, and opinions.

## How to install and configuration
To install and configure this application before running, relate to this guide
- [Installation and configuration](./Installation.md)

## How to Run
1.Start the virtual environment
```sh
source env/bin/activate
```
On Microsoft Windows:
```sh
. env/bin/activate
```
2.Set values for externalized variables

create file name `.env` to configuration **note that you may get your secretkeys [here](https://djecrety.ir)**

`.env` file template looks like [sample.env](sample.env) you can modify value and copy it into `.env`

3.Install requirements inside the virtual environment:
```sh
pip install -r requirements.txt
```
4.Run migrations
```sh
python3 manage.py migrate
```
5.Run tests
```sh
python3 manage.py test
```
6.Install data from the data fixtures
```sh
python3 manage.py loaddata data/all_data.json
```
7.Run the application
```sh
python3 manage.py runserver
```
Then, go to `http://127.0.0.1:8000/` or `localhost:8000/` for application.

8.Exit the virtualenv
```sh
deactivate
```

## Project Documents

All project documents are in the [Project Wiki](https://github.com/thanidacwn/veggie-hub/wiki).