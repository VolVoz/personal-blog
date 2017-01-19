# Flask personal blog

[![Code Health](https://landscape.io/github/VolVoz/personal-blog/master/landscape.svg?style=flat)](https://landscape.io/github/VolVoz/personal-blog/master)
[![Build Status](https://travis-ci.org/VolVoz/personal-blog.svg?branch=master)](https://travis-ci.org/VolVoz/personal-blog)
[![Coverage Status](https://coveralls.io/repos/github/VolVoz/personal-blog/badge.svg?branch=master)](https://coveralls.io/github/VolVoz/personal-blog?branch=master)

## Setup

```
git clone https://github.com/VolVoz/personal-blog.git
cd personal-blog/
```

## Make virtualenv

```
virtualenv -p env
source env/bin/activate
```

## Install requirements

```
pip install -r requipments/requirements.txt
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

### TODO:

- [x] Add base unittests
- [x] Launch unittests on the Travis-CI
- [ ] Add site search tool
