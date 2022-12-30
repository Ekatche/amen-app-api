# amen-app-api
Amen is a e-commerce api app 

# before pushing to Github 

To reformat the repo 
`` docker-compose run --rm app sh -c "black ../app"``  

To perform linting 
`` docker-compose run --rm app sh -c "flake8" ``

# to start self hosted runner for Github actions 
get in the actions runner dir
`` cd actions-runner``  
start the actions runner

`` ./run.sh``

