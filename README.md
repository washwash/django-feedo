# Feedo
Simple RSS reader backend

## Explanation

## Instalation
Easy peasy lemon squeezy, but here is the thing - Docker and Docker Compose 
should be installed properly. Pls, check [Starred](##starred) section.

Okay, now run three commands:
```
git clone https://github.com/washwash/django-feedo.git
cd django-feedo/
docker-compose up
```
_beep beep boop beep boop_

After that, open another terminal tab and run
```
docker ps --format '{{.Names}}'
```
Everithing is okay if you can see something like that
```
>docker ps --format '{{.Names}}'
djangofeedo_nginx_1
djangofeedo_celery_1
djangofeedo_application_1
djangofeedo_db_1
djangofeedo_rabbit_1
```

Now, open a browser and get the Feedo on 127.0.0.1!

## Testing
Just build `feedo` and `db` containers and run `test`
```
docker-compose run test
```


## Starred:
_or it works on my local machine_
* Python 3.6.8
* Docker 17.12.0-ce
* docker-compose 1.17.0
* Ubuntu 16.04


## License
[MIT](https://choosealicense.com/licenses/mit/)