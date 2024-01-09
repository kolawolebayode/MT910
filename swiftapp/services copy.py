import glob
import os
import logging
from datetime import datetime
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from .models import Acct, Transactions, Ref, UnMatchedTransaction
import pysftp
from decouple import config
logger = logging.getLogger('django')

Hostname = "91.226.24.226"
Username = "UBACGB2L_FIN"
Password = "mdFrI6rLF9"
remoteFilePath = f"FIN/FromSWIFT/MT910"
localFilePath = 'C:\Application\swiftproject\sftp_folder1'  #\MT_08093148_3977.txt'
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
# Create your views here.

def readfile():

    # catch exception here#
    with pysftp.Connection(host=Hostname, username=Username, password=Password, cnopts=cnopts)  as sftp: 
        print("Connection successfully established")
        print("Processsinng ... ")
        #with sftp.cd('FIN/FromSWIFT/MT910') as dir:             # temporarily chdir to public

        #### Configure for the different Units here
        #refs = Ref.objects.filter(team = 'Trade Operations')
        #print(sftp.listdir('/FIN/FromSWIFT/MT910'))

        for obj in sftp.listdir(remoteFilePath):
          
            file_name = obj
            remotefile = f"{remoteFilePath}/{obj}"
            if obj.endswith('txt'):
            
               
                with sftp.open(remotefile, 'r', 32768) as f:
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
                  
    
                    sender_info = str(sender_info).replace("[", "")
                    sender_info = str(sender_info).replace("]", "")   
                    sender_info = str(sender_info).replace(":72:", "")     
                    sender_info = str(sender_info).replace("'//", "\n")  
                   
                    all_data = {}
        
                    for item in output:
                        item = item.strip() 
                        
                        if not item.startswith("-}{5:") and not item.startswith("-}{5:") and not item.startswith("//"):
                            
                            if item.startswith("{1:"):
                                all_data.update({"header1":item})
                                ordering_customer = item[6:18]
                                all_data.update({"ordering_customer":ordering_customer})
                            if ":20:" in item:
                                senders_ref = item.replace(":20:", "")
                                all_data.update({"senders_ref":senders_ref})
                            if ":21:" in item:
                                mt103_related_ref = item.replace(":21:", "")
                                all_data.update({"mt103_related_ref":mt103_related_ref})
                            if ":25:" in item:
                                 
                                account_id = item.replace(":25:", "")
                                all_data.update({"account_id":account_id})
                            if ":32A:" in item:
                                value_date_and_tran_amount = item.replace(":32A:", "")
                                if "," in value_date_and_tran_amount:
                                    value_date_and_tran_amount = value_date_and_tran_amount.replace(",","")
                                value_date = value_date_and_tran_amount[:6]
                                value_date_str = datetime.strptime(value_date, '%y%m%d').strftime('%Y-%m-%d')
                                currency = value_date_and_tran_amount[6:9]
                                trans_amount = value_date_and_tran_amount[9:]
                                all_data.update({ "value_date_and_tran_amount":value_date_and_tran_amount, "value_date":value_date, 'value_date_str': value_date_str, "currency":currency, "trans_amount":trans_amount })
                            if ":52A:" in item:
                                ordering_institution = item.replace(":52A:", "")
                                all_data.update({"ordering_institution":ordering_institution})
                            if ":56A:" in item:
                                intermidiary = item.replace(":56A:", "")
                                all_data.update({"intermidiary":intermidiary})
                            if ":72:" in item:
                                sender_info =  sender_info                       


                              
                   
                    #mt103_related_ref = all_data.get('mt103_related_ref')
                    
                    #### Configure for the different Units here
                    #for team in ['Trade Operations']:
                 
                    team = 'Trade Operations'
                    refs = Ref.objects.filter(team = team )
                    #if refs:
                    for item in refs:
                        
                        if  mt103_related_ref.startswith(item.reference):
                            try:
                                Transactions.objects.create(
                                                                file_name = file_name,
                                                                senders_ref = all_data.get('senders_ref'),
                                                                value_date_and_tran_amount = all_data.get('value_date_and_tran_amount'),
                                                                value_date = all_data.get('value_date_str'),
                                                                currency = all_data.get('currency'),
                                                                trans_amount = all_data.get('trans_amount'),
                                                                ordering_institution = all_data.get('ordering_institution'),
                                                                mt103_related_ref = mt103_related_ref,
                                                                account_id = all_data.get('account_id'),
                                                                intermidiary = all_data.get('intermidiary'),
                                                                team = team,
                                                                header1 = all_data.get('header1'),
                                                                footer = footer,
                                                            
                                                                ordering_customer = all_data.get('ordering_customer'),
                                                                sender_receiever_info = sender_info      
                                                        )
                                sftp.rename(remotefile, remotefile+"_"+str(team))
                                    

                            except Exception as e:  
                                print(e)
                                logger.info(f"{e}")
                                                    
                                    
                            
                    #configure for other teams here
                                  
                    # else:
                    #         ### This is temporary to store mt910 that were not for trades and are unprocesed
                    #         for item in refs:
                    #             print(item.reference)
                    #             if not  mt103_related_ref.startswith(item.reference):
                    #                 try:
                    #                     UnMatchedTransaction.objects.create(
                    #                                                     file_name = file_name,
                    #                                                     senders_ref = all_data.get('senders_ref'),
                    #                                                     value_date_and_tran_amount = all_data.get('value_date_and_tran_amount'),
                    #                                                     value_date = all_data.get('value_date_str'),
                    #                                                     currency = all_data.get('currency'),
                    #                                                     trans_amount = all_data.get('trans_amount'),
                    #                                                     ordering_institution = all_data.get('ordering_institution'),
                    #                                                     mt103_related_ref = mt103_related_ref,
                    #                                                     account_id = all_data.get('account_id'),
                    #                                                     intermidiary = all_data.get('intermidiary'),
                    #                                                     team = 'not set',
                    #                                                     header1 = all_data.get('header1'),
                    #                                                     footer = footer,
                    #                                                     # reciever_bic = reciever_bic,
                    #                                                     ordering_customer = all_data.get('ordering_customer'),
                    #                                                     sender_receiever_info = sender_info )
                    #                     sftp.rename(remotefile, remotefile+"_unprocessed")
                                    
                    #                 except Exception as e:    
                    #                     logger.info(f"{e}")  

                                

    return JsonResponse({"status": "completed"})  





