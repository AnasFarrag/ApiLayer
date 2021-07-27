
from flask import Flask
from urls import load_apps
from flask_restful import Api
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import settings
from datetime import datetime



# CLOUD Login
def login_to_cloud():
    settings.CLOUD.login(settings.CLOUD_USERNAME, settings.CLOUD_PASSWORD)
    print("logged in")
    return True

# Create CLOUD Dirs
def create_cloud_dirs():
    date_now = datetime.now()
    current_year = date_now.year
    current_month = date_now.month

    settings.YEAR = current_year
    settings.MONTH = current_month

    year_dir = settings.USERS_BASE_DIR_IN_CLOUD + str(settings.YEAR)
    month_dir = year_dir + '/' + str(settings.MONTH)

    try:
        settings.CLOUD.mkdir(year_dir)
        print('create year')
    except Exception as e:
        print('year already exist')
        pass

    try:
        settings.CLOUD.mkdir(month_dir)
        print('create month')
    except Exception as e:
        print('month already exist')
        pass

    else:
        print('date not changed')

# CLOUD LOGIN and Create Dirs ( Login Every 1 Hour)
def invoke_cloud_login_and_create_dirs():
    if login_to_cloud():
        create_cloud_dirs()


def create_app(name):

    app = Flask(name)

    #set RESTFul API
    api = Api(app)

    # load installed apps
    api = load_apps(api)

    # # load .env variables
    # load_dotenv('.env')

    #set configuration environment
    app.config.from_object('config.'+ settings.ENV)

    # set CORS origin and Allowed Hosts
    CORS(app)

    # initialize scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(invoke_cloud_login_and_create_dirs, trigger='interval', hours=1)
    scheduler.start()

    try:
        # To keep the main thread alive
        return app
    except:
        # shutdown if app occurs except
        scheduler.shutdown()


app = create_app(__name__)

if __name__ == '__main__':
    app.run()
