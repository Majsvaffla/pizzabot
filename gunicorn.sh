#! /bin/sh
exec pipenv run gunicorn pb.conf.wsgi --bind unix:/home/pizzabot/pizza.socket --access-logfile /home/pizzabot/pizza.log --workers 2
