# amen-app-api
Amen is a e-commerce api app 

# backend

to run server 
`` docker-compose run --rm app sh -c "python manage.py runserver"``
  
to reformat the repo 
`` docker-compose run --rm app sh -c "black ../app``  
to perform linting 
`` docker-compose run --rm app sh -c "flake8" ``