# Pedal

# Summary of the Project
The implementation of bike-sharing has solved the problem of short distance travel in cities, and it has greatly improved the existing urban public transport system. This flask project is a web-based application build to implement a bike-sharing platform called ‘Pedal’. In this application, customers can book and return a bicycle to rent as well as pay for their journey and report if a bicycle is defective in some manner. Operators will easily be able to track the bicycles for maintenance purposes and for the ability to repair and move bicycle between location. Finally, managers can effectively utilise certain data analysis techniques to see information on bike activities. The application referred in this repository is a user-friendly webpage which can effectively serve the customer, operator, and manager in their various roles and responsibilities.


# Installation
>>>
git clone https://stgit.dcs.gla.ac.uk/2684995a/pedal.git bikerental

cd bikerental

pip install -r requirements.txt

$ export FLASK_APP=bikerental.py

For Windows system when running on cmd use "set" instead of "export" in the command above

$ flask run
>>>

# Folder Structure
>>>
bikerental
|
├── app # main project folder  
│   ├── __init__.py  
│   ├── api # for api calls  
│   │   ├── __init__.py  
│   │   ├── bike.py # contains the api logic  
│   │   └── errors.py  
│   ├── app.db  
│   ├── app.db-journal  
│   ├── bikeCountTable.py # contains logic to return bike count in Flask-Table Format  
│   ├── bikeDB.py # contains logic to make DB call for Bike Table updates  
│   ├── bikeTable.py # contains logic to return available bikes in Flask-Table Format  
│   ├── bikerental.db  
│   ├── config.py # config file of the project  
│   ├── dbOperations.py # contains logic to implement generic db operations like a wrapper class  
│   ├── defective_bike.py # contains logic to return defective bikes in Flask-Table Format  
│   ├── forms.py # Flask WTForms are mentioned in this file  
│   ├── models.py # contains DB models classes  
│   ├── repairedBikes.py # contains logic to return repaired bikes in Flask-Table Format  
│   ├── routes.py # contains all the urls used to build this project as microservice app  
│   ├── static # contains all static files  
│   │   ├── attachment  
│   │   ├── bootstrap-4.1.3-dist  
│   │   ├── css  
│   │   │   └── main.css  
│   │   ├── fontawesome-free-5.9.0-web  
│   │   ├── img  
│   │   └── js  
│   │       ├── jquery-3.4.1.min.js  
│   │       ├── main.js  
│   │       ├── plotly-2.4.2.min.js  
│   │       ├── popper.js  
│   │       └── popper.min.js.map  
│   ├── templates # all jinja2 html template is stored in this location  
│   │   ├── _displayImage.html  
│   │   ├── base.html  
│   │   ├── body.html  
│   │   ├── dash.html  
│   │   ├── index.html  
│   │   ├── list.html  
│   │   ├── login.html  
│   │   ├── registration.html  
│   │   └── user # contains more  user specific htmml template  
│   │       ├── customer_dash.html  
│   │       ├── loadOperator.html  
│   │       ├── manager_charts.html  
│   │       ├── manager_dash.html   
│   │       ├── movecycle.html  
│   │       ├── operator_dash.html  
│   │       ├── report_defective.html  
│   │       └── trips.html  
│   ├── userDB.py # user database logic  
│   └── utility.py # utility to return json file based on role to render UI dynnamically  
├── bikerental.py  
├── bikerental_venv  
├── logs  
│   ├── bikerental.log  
├── migrations  
└── requirements.txt  
>>>
# Built With
- Flask and respective Flask libraries for database connection and integration of frontend webpages
- Python 3.7.3


# Hosted URL
The project is hosted on Heroku, please find the below link to access the webiste:
[https://pedal-flask.herokuapp.com/login](https://pedal-flask.herokuapp.com/login)

# Gitlab URL
The project GitLab URl:
[https://stgit.dcs.gla.ac.uk/2684995a/pedal](https://stgit.dcs.gla.ac.uk/2684995a/pedal)