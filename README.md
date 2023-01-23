# amen-app-api

Amen is a e-commerce api app

<a href="https://lucid.app/lucidchart/41e6c830-de76-4835-bab7-a846e6f195d6/edit?page=0_0&invitationId=inv_7beaef43-08ab-4bb3-a02f-49a69f8e89cc#"> Database schema</a>

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

