## Local run

You will need Python 3.11+ on your local pc. Go to project package in your terminal
```
cd path_to_ptogect
```
### 1.Install pip, requirements and environment
``` 
python -m pip install
pip install -r requirements.txt
``` 
For environment variables create file with title ".env" with the same data as .env.template.
Set BASE_DOMAIN=http://127.0.0.1:8000 there
### 2.Run the server with:
``` 
uvicorn xm.orders:app --reload
``` 
### 3.Check it
Open your browser at http://127.0.0.1:8000/orders/1

You will see the JSON response as:
``` 
{"id": 1, "product_name": "Product A", "quantity": 10}
``` 
### 4.Interactive API docs
Now go to http://127.0.0.1:8000/docs 

### 5.Run tests using pytest with different options

#### From the project root run command. 
``` 
pytest .
``` 
All tests should be executed in 4 threads
#### From the project root run command. 
``` 
pytest . -n2
```
All tests should be executed in 2 threads

You can pass different option to run different sets of tests.
For example pass a specific test module title:
```
pytest ./tests/test_orders.py
```
or
```
pytest ./tests/test_acceptance.py
```
or run tests that match a specific substring:
```
pytest -k <substring>
```
### 6. Get the allure report of tests
#### From the project root run command. 
```
allure serve
```
Browser with allure report will be started 
![Allure report](\xm-tests\report_examples\allure_report_1.png "Allure report")
![Allure report](\report_examples\allure_report_2.png "Allure report")

## Run in Docker

### 1.Create docker image
From the project directory execute the command in terminal 
``` 
docker build --tag xm-tests .
``` 
### 2. Run the docker container 
```
docker run -p 8000:8000 --env-file=.env xm-tests
```
Now the application is started in docker container. Go to http://127.0.0.1:8000/orders/1 to check it
You will see the JSON response as:
``` 
{"id": 1, "product_name": "Product A", "quantity": 10}
``` 
### 3. Then you are able to run the tests and get allure report
#### From the project root run command. 
``` 
pytest .
``` 
or other command mentioned above

### 4. Get the allure report of tests
#### From the project root run command. 
```
allure serve
```
Browser with allure report will be started 
![Allure report](\xm-tests\report_examples\allure_report_1.png "Allure report")
![Allure report](\report_examples\allure_report_2.png "Allure report")