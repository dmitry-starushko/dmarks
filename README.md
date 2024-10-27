# DMarks NG Project
##  Deploy

- Ensure statics collected with `manage.py collectstatic`
- Copy project to docker host
- Set appropriate value for CSRF_TRUSTED_ORIGINS in `settings/prod.py` 
- Then on docker host:  
    - `docker-compose up -d --build`
    - `docker-compose exec web python manage.py migrate`
    - `docker-compose exec web python manage.py loaddata initial-data.json`
    - `docker-compose exec web python manage.py createsuperuser`
    - `docker-compose exec web ln -sf addons/libtransmutation.so.1.0.0 transmutation.so`
    - `docker-compose restart`