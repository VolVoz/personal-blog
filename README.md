# Flask personal blog

[![Code Health](https://landscape.io/github/VolVoz/personal-blog/master/landscape.svg?style=flat)](https://landscape.io/github/VolVoz/personal-blog/master)

## Setup

```
git clone https://github.com/VolVoz/personal-blog/
cd personal-blog/
```
Make virtualenv
```
virtualenv -p env
source env/bin/activate
```
Install requirements
```
pip install -r requirements.txt

```
Do not forget to set environment variables for the following parameters
```
export APP_SETTINGS=config.StagingConfig
export DATABASE_URL='postgresql://DB_USERNAME:DB_PASSWORD@localhost/DB_NAME'
export GMAIL_USER=your_mail@adress
export GMAIL_PASS=mail_pass
export SECRET_KEY=some_secret_key
export ADMIN_PASSWORD=password

```
For run app:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py runserver
```

#### TODO:

- [ ] Documentation for deploying to heroku
- [ ] Launch unittests on the Travis-CI
- [ ] Add site search tool
