import glob
import os
import logging
from datetime import datetime
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from .models import Acct, Transactions, Ref, UnMatchedTransaction

from .processfile import fileprocessor
from decouple import config
logger = logging.getLogger('django')


#remoteFilePath = config('remoteFilePath')
remoteFilePath = "/home/ubauk-admin/MT910"
localFilePath = config('localFilePath')  #\MT_08093148_3977.txt'

# Create your views here.

def readfile():
    print('start reading')
    # catch exception here#
    try:
        
        print("Connection successfully established")
        print("Processsing ... ")
    

        for obj in os.listdir(remoteFilePath):
            print(obj)
        
            file_name = obj
            remotefile = f"{remoteFilePath}/{obj}"
            if obj.endswith('txt'):
            
            
                with open(remotefile, 'r', 32768) as f:
                    output = f.readlines()   
                    sender_info = []
                    for item in output:
                        # Strips the newline character
                        item = item.strip()
                        if item.startswith("//"):
                            sender_info.append(item)
                        if item.startswith(":72:"):
                            sender_info.append(item)
                        if item.startswith("-}{5:"):
                            footer = item
                        
                    f.close()

                    #File processor view
                    response = fileprocessor(output, sender_info)

                    
                    #### Save all details in mt910 into DB
                    try:
                        Transactions.objects.create(
                                                        file_name = file_name,
                                                        senders_ref = response['all_data'].get('senders_ref'),
                                                        value_date_and_tran_amount = response['all_data'].get('value_date_and_tran_amount'),
                                                        value_date = response['all_data'].get('value_date_str'),
                                                        currency = response['all_data'].get('currency'),
                                                        trans_amount = response['all_data'].get('trans_amount'),
                                                        ordering_institution = response['all_data'].get('ordering_institution'),
                                                        mt103_related_ref = response['mt103_related_ref'],
                                                        account_id = response['all_data'].get('account_id'),
                                                        intermidiary = response['all_data'].get('intermidiary'),
                                                        team = 'unsorted',
                                                        header1 = response['all_data'].get('header1'),
                                                        footer = footer,
                                                    
                                                        ordering_customer = response['all_data'].get('ordering_customer'),
                                                        sender_receiever_info = sender_info      
                                                )
                        os.rename(remotefile, remotefile+"_processed")
                        team = 'Trade Operations'
                        refs = Ref.objects.filter(team = team )
                        for item in refs:  
                            # Filter for the various teams here and update DB (Allows for filtering) 
                            if  response['mt103_related_ref'].startswith(item.reference):
                                Transactions.objects.filter(mt103_related_ref= response['mt103_related_ref']).update(team=team )
                    except Exception as e:  
                        print(e)
                        logger.info(f"{e}")  
    except Exception as e:
        print(e)                 

    return JsonResponse({"status": "completed"})  





