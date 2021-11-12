'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
APPLICATION FOR DEPLOYING the Carbon Footprint Calculator code in IBM Cloud
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


'''-----------------------------
A. Import necessary libraries 
-----------------------------'''
import os
from pathlib import Path
from flask import Flask, render_template, request,url_for,redirect
from werkzeug.utils import secure_filename
import pandas as pd
import sqlite3
from flask_login import LoginManager
import datetime
# Internal imports
from db import init_db_command
from user_sql import User
from scripts.barcode_scanner import BarcodeDecoder
import matplotlib.pyplot as plt
'''-----------------------------
B. Import Paths 
-----------------------------'''
currentDirPath = os.path.dirname(os.path.realpath(__file__))
sourcePath = Path(currentDirPath)
dataPath=sourcePath/"data"
co2_source_file = pd.read_excel(os.path.join(dataPath, "co2_impact_spending.xlsx"))

#uploadPath=os.path.join(str(sourcePath),"data","uploads") #Local usage
#uploadPath = '/tmp/'
try:
    os.mkdir('./tmp')
except OSError as error:
    pass
uploadPath = './tmp'
staticPath = './static'

#DataBase for reporting
'''-----------------------------
C. App Config 
-----------------------------'''
app = Flask(__name__)
# Flask app setup
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = uploadPath
app.config['PICTURE_FOLDER'] = staticPath

# User session management setup
login_manager = LoginManager()
login_manager.init_app(app)
# Naive database setup : to create the database used for storing user ID's
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass
# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))
'''-----------------------------
D. App Core Functions 
-----------------------------'''

#1.Home and core function : Sign in with google and when ok, access homepage.
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        #fetch credentials from DB
        else:
            return render_template('home.html', error=error,url_chart=os.path.join(app.config['PICTURE_FOLDER'],'new_plot.png'))
    return render_template('login.html', error=error)

#4. Get calculator results
@app.route("/upload",methods=['GET','POST'])
def setup_upload():
    return render_template('upload.html')

@app.route("/result",methods=['POST'])
def returnPrediction():
    if request.method == 'POST':
        if 'file_upload_form' in request.form:
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(str(app.config['UPLOAD_FOLDER']), filename))
            filePath = os.path.join(str(app.config['UPLOAD_FOLDER']), filename)
            barcode = BarcodeDecoder(filePath,user_location="Brussels,Belgium")
            os.remove(os.path.join(str(app.config['UPLOAD_FOLDER']), filename))
            return render_template("result.html", prediction="{}".format(barcode))

@app.route("/spendings_form",methods=["POST","GET"])
def calculate_score():
    if request.method == 'POST':
        checked=(request.form.getlist('form'))
        #get C02
        emissions = co2_source_file[co2_source_file['BOX'].isin(checked)]
        emissions=pd.Series([emissions["TONS_CO2"]], dtype="float64").sum()
        emissions=sum(emissions)
        #add to DB
        # Export to dataframe with date of request
        date_run = datetime.date.today()
        weekyear=str(date_run.isocalendar()[1])+"_"+str(date_run.year)
        user_df = pd.DataFrame({"REQUEST_DATE": date_run,
                                "REQUEST_WEEK":weekyear,
                                "CARBON_SCORE":emissions}, index=[0])
        columns_df = ["REQUEST_DATE", "REQUEST_WEEK", "CARBON_SCORE"]
        user_df = user_df.reindex(columns=columns_df)
        #Generate plot
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'score_log.csv')
        if not os.path.exists(output_dir):
            user_df.to_csv(os.path.join(output_dir), sep=";", decimal=",")
        else:
            user_df.to_csv(output_dir, mode="a", sep=";", header=None)
        user_df = pd.read_csv(output_dir, sep=";")
        # sorting by first name
        user_df.sort_values("REQUEST_WEEK", inplace=True)        # dropping ALL duplicate values
        user_df.drop_duplicates(subset="REQUEST_WEEK",keep='last', inplace=True)
        plt.plot(user_df["REQUEST_WEEK"], user_df["CARBON_SCORE"])
        plt.xlabel("Week")
        plt.ylabel("Carbon generated")
        plt.savefig(os.path.join(app.config['PICTURE_FOLDER'],'new_plot.png'))
        return render_template('/home.html', url_chart=os.path.join(app.config['PICTURE_FOLDER'],'new_plot.png'))

    return render_template("spendings_form.html")


if __name__ == "__main__":
    app.run(debug=True)