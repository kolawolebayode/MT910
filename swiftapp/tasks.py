import requests
import schedule
import time
# from apscheduler.schedulers.background import BackgroundScheduler
# from .jobs import schedule_api
from decouple import config
from schedule import repeat, every
from swiftapp.services import readfile
from swiftapp.payment import Payment


app_url = config('app_url')


def transaction_process_task():
    # url=f"{app_url}/api/processing"
    # response = requests.get(url)   
    print("trrtrtrt")


def transaction_process_task_hook(task):
    print(task.result)


