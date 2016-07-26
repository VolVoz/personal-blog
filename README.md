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
Create a postgres database

Do not forget to set environment variables for the following parameters in **'import_envs.sh'** and run:
```
source import_envs.sh
```

Run the migrations initialize Alembic:
```
python manage.py db init
```
Create migration by running the **db migrate** command:
```
python manage.py db migrate
```
Apply the upgrades to the database using the **db upgrade** command::
```
python manage.py db upgrade
```
For run app:
```
python manage.py start
```

#### TODO:

- [ ] Documentation for deploying to heroku
- [ ] Launch unittests on the Travis-CI
- [ ] Add site search tool
