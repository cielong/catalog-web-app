# Catalog Web Application
This Catalog Web Application is intended to provide the users useful description of items in different categories. Currently, this web app contains some information about Animation and Mysterious, which are areas I personally interested in. If you are also interested in these topics I provided, don't hesitate to check the demo version on heroku [Catalog Web App](http://catalog-web-app.herokuapp.com). However, all the data are copied directly from its according wikipedia page, thus nothing new there.  

This web app is implemented in python3 using Flask, SQLAlchemy and WTForms. The web app also provides user authentication and authorization, taking advantages of Oauth2 and Google Sign In.  

## Getting started
### Prerequisites
To run the server code, it is recommended to use a virtual enviroment, and a *Pipfile* (for more infomation, check [Pipenv](https://docs.pipenv.org)) has been provided.  
In order to use the Pipfile to set up the vitual environment, you have to first install pipenv  
> pip install pipenv

After successfully installed, run the following command to set up Virtual Enviroment and install necessary packages:  

> pipenv install

**IMPORTANT**  
In order to conform to Heroku deployment, the codes utilize some environment variables (DATABASE_URL, PORT etc.), and you can set these in virtual environment by providing a *.env* file under the catalog directory. An example file *.env-example* has been provided, and you'll have to refer to it to set up your own enviroment variables.  

Then, to start the virtual environment, use
> pipenv shell

And later exit it use, 
> exit

### Set up database and some fake items
You'll have to first set up the database before running the server.  
The file *database_setup.py* contains a simple model to represent data (Item, Category, References, User and there relationships). 
> python database_setup.py

The file *fakeItems.py* provides some initial data and also a default user has been set up.  
> python fakeitems.py

### Run the server in localhost
After run the above, you will be able to run the server in command line, the following command provide and example.
> python catalog.py --host 0.0.0.0 --port 5000
