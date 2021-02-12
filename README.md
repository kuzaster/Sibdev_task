# How to run RestAPI service:

 - Install [Python 3.8](https://www.python.org/downloads/), [Docker](https://docs.docker.com/engine/install/), 
   [Docker-compose](https://docs.docker.com/compose/install/) on your computer, if you haven't.
- Clone or download project from GitHub [repository](https://github.com/kuzaster/Sibdev_task)
- Open terminal
- Go to the main directory of the project, where you can see Dockerfile and docker-compose.yml 
- Run `docker-compose up` and wait a little, while building and running container with service
- Enter http://localhost:8000/api/v1/deals/ in a browser to see the service running

P.S.
You can run `docker-compose up -d` to start up service in background and free your terminal. 

# How to work with RestAPI service:

- Run service and open main page (http://localhost:8000/api/v1/deals/) in your browser
- You can see "GET" and "POST" endpoints
- Push the button `Browse` in "POST" endpoint and chose .csv file to upload
- Push the button `POST` and wait a little
- You will see the message `"OK - файл был обработан без ошибок"` if succeed or message of error otherwise
- Push the button `GET` and you will see top 5 customers and there filtered gems.
- To stop service go back to your terminal and push `Ctrl+C` on your keyboard 
  or run `docker-compose stop` if you run service in background