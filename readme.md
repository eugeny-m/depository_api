# Depository API

#### How to run:

* download and install docker (https://www.docker.com/products/docker-desktop)
* Clone project from github
`git clone git@github.com:eugeny-m/depository_api.git`
* Go to project root `cd depository_api`
* build image `docker-compose build`
* run docker containers `docker-compose up -d`

##### First Run

* run migrations `docker exec depository_api_depository_api_1 python manage.py migrate`
* generate test data `docker exec depository_api_depository_api_1 python generate_test_data.py --users_count 20000 --operations_count 10`

#### Endpoints

* http://0.0.0.0:8000/api/v1/accounts/ (User Account List Viewset List)
* http://0.0.0.0:8000/api/v1/accounts/<account_id>/monthly-report/<int:year>/<int:month> (Monthly report of user account operations)
