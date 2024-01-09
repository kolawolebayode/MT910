import requests
#import schedule
import time
from decouple import config
from swiftapp.services import readfile
from swiftapp.payment import Payment


app_url = config('app_url')


def process_task():

   named_tuple = time.localtime() # get struct_time
   time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
   print(time_string)

   ##url=f"{app_url}/api/processing" #main working one
   # url=f"{app_url}/api/fileprocess" 
   # response = requests.get(url)  
   # print(url)
  
