# Context:

This project is an example of implementation of Carbon Footprint Calculator and deployed on IBM Cloud.
It uses the functions previously created to score a week's consumption into a carbon footprint.
It also allows for the reading of a barcode to determine the origin of a product and compute the distance it travalled

Main features of the app:
* Deployed in couple of lines of code
* Able to calculate Carbon Footprint based on questionaire
* Integrates Barcode Scanner to define country of origin of products
# Structure:

The code is structured as follows:
* app.py contains the core functions of the app, including the configuration of the app, the necessary imports and the execution of the prediction
* app.yaml is the app configuration file necessary for the setup of the project 
* user_sql.py is the code used for initializing the database and record the user's info following the  sign-in
* requirements.txt displays the necessary libraries and packages to run this app
* templates/ contain the HTML templates used for the front of this project


To run the code locally:
    * `set FLASK_APP=app.py` 
    * `python -m app`

  
  
