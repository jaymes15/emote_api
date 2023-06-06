#!/bin/bash

heroku config:set DEBUG=$DEBUG --app $HEROKU_APP
heroku config:set ALLOWED_HOSTS=$ALLOWED_HOST --app $HEROKU_APP
heroku config:set SECRET_KEY=$DJANGO_SECRET_KEY --app $HEROKU_APP
heroku config:set DJANGO_SETTINGS_MODULE=$SETTINGS_MODULE --app $HEROKU_APP
heroku config:set CLOUDINARY_CLOUD_NAME=$CLOUDINARY_CLOUD_NAME --app $HEROKU_APP
heroku config:set CLOUDINARY_API_KEY=$CLOUDINARY_API_KEY --app $HEROKU_APP
heroku config:set CLOUDINARY_API_SECRET=$CLOUDINARY_API_SECRET --app $HEROKU_APP
heroku config:set IS_CLOUDINARY=$IS_CLOUDINARY --app $HEROKU_APP
heroku config:set REDIS_NETWORK=$REDIS_NETWORK --app $HEROKU_APP

heroku run python manage.py collectstatic --noinput --app $HEROKU_APP
heroku run python manage.py makemigrations --app $HEROKU_APP
heroku run python manage.py migrate --app $HEROKU_APP




