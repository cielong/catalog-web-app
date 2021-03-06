# Catalog Web Application
This Catalog Web Application is intended to provide the users useful description of items in different categories. Currently, this web app contains some information about Animation and Mysterious, which are areas I personally interested in.  

If you are also interested in these topics I provided, don't hesitate to check the demo version on heroku [Catalog Web App](http://catalog-web-app.herokuapp.com). However, all the data are copied directly from its according wikipedia page, thus nothing new there.  

## API Usage Description
### JSON End Points (API)
There are three json endpoints api could be used in this web app, namely request information for the whole catalog, a specific category and a specific item.   

| JSON EndPoints | Description |
| -------------- | ----------- |
|/catalog.json|To retrieve all the items' information in the catalog|
|/catalog/\<category-name\>.json|To retrieve all the items' information for category with name \<category-name\>|
|/catalog/\<category-name\>/\<item-name\>.json|To retrieve all the items' information for item with name \<item-name\> and  category name \<category-name\>|


## Implementation Intro
The web app is implemented in python3 using Flask, SQLAlchemy and WTForms.  
The web app also provides user authentication and authorization, through local permission system and Google Sign In using OAuth2.  

**NOTICE!**   
The Google SignIn won't work locally unless a .env file has been correctly setup under the directory catalog, see below [Enable OAuth2/Google SignIn](#enable-oauth2google-signin-opional).  

## Setting up server on local system
### Prerequisites
The web app is written in python3, however, it should work with python2 (If you have set up the virtual enviroment, this won't be your worry). All the required package has been provided in the *Pipfile*, and see [Set up virtual environment](#set-up-virtual-environment) for how to use it. 

### Download/Clone this repo to your local computer
> git clone git@github.com:cielong/catalog-web-app.git

And then, change directory to the cloned repo.

### Set up virtual environment
#### Install required python libraries
To run the server code, it is recommended to use a virtual enviroment, and a *Pipfile* (for more infomation, check [pipenv](https://docs.pipenv.org)) has been provided.  
In order to use the Pipfile to set up the vitual environment, you have to first install pipenv  
> pip install pipenv

After successfully installed, run the following command to set up Virtual Enviroment and install necessary packages:  

> pipenv install

#### Set up .env file (IMPORTANT!!)
In order to conform to Heroku deployment, the codes utilize some environment variables (DATABASE_URL, PORT etc.).  

You can set these variables in virtual environment by providing a **.env** file under the catalog directory, and the virtual environment will automatically take use of it when it starts (see [next section](#start-virtual-environment)). 

Because of private information in such file, only an example file **.env-example** has been provided, and you'll have to refer to it to write your own **.env** file in order to set up these required enviroment variables.  

#### Start virtual environment
Then, to start the virtual environment, use
> pipenv shell

And later to exit the virtual environment, use, 
> exit

### Set up database and add some fake items
You'll have to first set up the database before running the server.  
The file *database_setup.py* contains a simple model to represent data (Item, Category, References, User and there relationships). 
> python database_setup.py

The file *fakeItems.py* provides some initial data and also a default user has been set up.  
> python fakeitems.py

### Enable OAuth2/Google SignIn (Opional)
You'll have to add more info in the *.env* file in order to make the Google Signin works. To do this, you'll have to set up your own web app in [Google API Console](https://console.cloud.google.com/apis/dashboard), for more information, check the the above link to understand how to register a web app.  

After registered, add the following line in the *.env* file
```shell
G_CLIENT_ID="YOUR GOOGLE CLIENT ID FOR YOUR WEB APP"
G_CLIENT_SECRET="YOUR GOOGLE CLIENT SECRET FOR YOUR WEB APP"
```

### Run the web app locally
After run the above, you will be able to run the server in command line, the following command provides an example command
> python catalog.py --host 0.0.0.0 --port 5000

## TODO
There are still a lot haven't been done:  
- [ ] Add more OAuth Providers and local permission system to provide json request only to login users.
- [ ] Add Profile and Forgot Password to allow user update their personal information.
- [ ] Add email confirmation techniques and update user model, to disallow invalid email addresses.
- [ ] Add image upload button and Add-More-Row, Remove-Row button to better add/edit the items.
- [ ] Add Search functionalities in the navbars.
- [ ] Add Developer Guide page and create developer-friendly instructions.
- [ ] Add some more javascript support.
