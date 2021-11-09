# Context:

This project is an example of implementation of Carbon Footprint Calculator and deployed on IBM Cloud.
It uses the functions previously created to score a week's consumption into a carbon footprint.
It also allows for the reading of a abrcode to determine the origin of a product

Main features of the app:
* Deployed in couple of lines of code
* Able to calcualte Carbon Footprint based on questionaire
* Integrates Barcode Scanner to define country of origin of produces
# Structure:

The code is structured as follows:
* app.py contains the core functions of the app, including the configuration of the app, the necessary imports and the execution of the prediction
* app.yaml is the app configuration file necessary for the setup of the project in GAE
* user_sql.py is the code used for initializing the database and record the user's info following the  sign-in
* requirements.txt displays the necessary libraries and packages to run this app
* templates/ contain the HTML templates used for the front of this project


To run the code locally:
    * `set FLASK_APP=app.py` 
    * `python -m app`

  
  
# Resources:

The main articles and blogs used to create this project can be found here:
* https://medium.com/@dmahugh_70618/deploying-a-flask-app-to-google-app-engine-faa883b5ffab
* https://www.jetbrains.com/help/pycharm/managing-dependencies.html?_ga=2.24775930.1189069863.1589890210-437005317.1589890210
* https://blog.cambridgespark.com/deploying-a-machine-learning-model-to-the-web-725688b851c7
* https://towardsdatascience.com/designing-a-machine-learning-model-and-deploying-it-using-flask-on-heroku-9558ce6bde7b
* https://medium.com/@jeremy.from.earth/google-cloud-storage-file-upload-with-flask-javascript-64ec5bc5c42d
* https://gist.github.com/merqurio/c0b62eb1e1769317907f
* https://pythonspot.com/login-to-flask-app-with-google/
* https://www.mattbutton.com/2019/01/05/google-authentication-with-python-and-flask/
* https://realpython.com/flask-google-login/
* https://github.com/blackmad/flask-google-login-example/blob/master/main.py

# Contact:

For more information about the app's content and usage, please contact Joëlle Van Damme at joelle.van.damme@be.ey.com