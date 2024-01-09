
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import process_task
import time
from time import sleep
from decouple import config




def start():
    #minute = 
    #hour =
    scheduler = BackgroundScheduler()
    
    #scheduler.add_job(process_task, 'interval', seconds=10, id='process1')#, replace_existing=True)
    #scheduler.add_job(process_task, day_of_week='mon-fri', hour='1-16', seconds='10', id='process1', jitter=10)
    scheduler.add_job(process_task, trigger='cron', day_of_week='sat-sun', hour='22-23', second='*/10', id='process1')
    scheduler.start()
    sleep(10)


     

    


