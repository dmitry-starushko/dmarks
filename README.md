# DMarks NG Project
##  How to deploy

- Ensure statics collected with `manage.py collectstatic`
- Copy project to docker host
- **Replace SECRET_KEY in `settings.prod.py` with NEW strong password and store it!** (for first time deploy only)
- Set appropriate value for CSRF_TRUSTED_ORIGINS in `settings/prod.py`
- Set correct TELEBOT env. var. om target host
- Then on docker host:  
    - `docker-compose up -d --build`
    - `docker-compose exec web python manage.py migrate`
    - `docker-compose exec web python manage.py loaddata initial-data.json`
    - `docker-compose exec web python manage.py createsuperuser`
    - `docker-compose exec web ln -sf addons/libtransmutation.so.1.0.0 transmutation.so`
    - `docker-compose restart`
- or:
    - `bash deploy`