Guide to learn the API:
Steps and Questions!

Get it running:
1. Get the code from Gitlab.
2. Install Python3 and dev kit etc. with venv, furthermore install httpie
3. run ./run.sh in the base folder and confirm that the API is running on localhost:8000
4. Type into another terminal window “http post ‘http://localhost:8000/v1/users/login user=’admin@example.com’ password=’admin’” and confirm that a token is returned.

Make yourself familiar:
4. Read http://www.restapitutorial.com/ to learn about rest API
5. Read http://www.hug.rest/ to make yourself familiar with the framework hug.
6. Install pycharme or an editor of your choice to open the project (backend-api).
7. find the file which includes the endpoints
*Tasks: 
1. What is the files name?
2. List the endpoints and its HTTP verbs.
3. What is a python decorator?
4. Try to explain the decorators of each method.
5. Add an extra GET endpoint /my/first/endpoint which return: “Hello World!”
6. Restart the API, use httpie and call your endpoint, confirm that the endpoint is working.*

Lets check on Influx Communication:
8. Find the file which handles the communication with influxDB.
9. Check if the method __conn_setup__(self, ssl=True): has SSL set to true by default if you want to use an influx instance with ssl configured
10. Check the config.ini file and confirm that the credentials there are valid for the used influxdb instance.
11. Make your self familiar with the influxdb methods.
Tasks:
7. Write an post endpoint in the api (i.e. as before with the /my/first/endopoint) which writes something into influxDB using the class InfluxDBWrapper.
8. Write an get endpoint in the api which gets something from the InfluxDb  using the class InfluxDBWrapper.
9. Compile the API and confirm that the endpoints are wokring.
10. Go to the influxDB Admin panel and confirm that the data is written to the correct database. 

