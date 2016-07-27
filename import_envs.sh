#!/bin/sh
echo === IMPORT ENVS ===
export APP_SETTINGS=config.StagingConfig
export DATABASE_URL='postgresql://DB_USERNAME:DB_PASSWORD@localhost/DB_NAME'
export GMAIL_USER=user@gmail.com
export GMAIL_PASS=mail_pass
export SECRET_KEY=some_secret_key
export ADMIN_PASSWORD=password
echo secret key: $SECRET_KEY
echo gmail password: $GMAIL_PASS
echo gmail account: $GMAIL_USER
echo database: $DATABASE_URL
echo app config: $APP_SETTINGS
echo app password: $ADMIN_PASSWORD
echo === DONE ===