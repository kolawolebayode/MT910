import requests
import json
from decouple import config
from django.http import HttpResponse, JsonResponse

from datetime import datetime
from .models import Acct, Transactions, Ref

payment_url = config('payment_url')
print(payment_url)


def gen_token():

    
    #url = "{payment_url}:8082/api/auth_token/"
    url = "http://172.19.60.30:8081/api/auth_token"


    payload = json.dumps(
                        {
                        "username": "admin",
                        "password": "admin"
                        }
                        )
    headers = {
                'Content-Type': 'application/json'
              }

    response = requests.request("POST", url, headers=headers, data=payload)
  
    return response.json()
    



def Payment():
    accounts = Acct.objects.all()
    response_token = gen_token()
    
    
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {response_token['access']}"
    }


    try:
        url = f"http://172.19.60.30:8081/api/transfer"
    except Exception as e:
        print(e)
        return JsonResponse({"error": e})
    
    get_entries = Transactions.objects.filter(status='pending').exclude(team='unsorted')
   # get_entries = Transactions.objects.filter(id='96')
    if not get_entries:
        return HttpResponse("No transactions")

    for entry in get_entries:
 
        for acct in accounts:
            if entry.currency == acct.currency: # Use here to differentiate wether trade ops or treasury ops to filter when needed
                nostro_acct = acct.account_num
                suspense = acct.suspense
 
                payload  =  {
                        "debit_acct": nostro_acct, # Get Debit account
                        "credit_acct": suspense,  # Get Credit account
                        "tran_amt": entry.trans_amount,   #Clean amount
                        "tran_crncy": entry.currency,   
                        "tran_particulars": entry.mt103_related_ref,
                        "tran_remarks": entry.mt103_related_ref     #entry.tran_particular[:20]  # Get Trans Remarks
                        }
                
                resp = requests.request("POST", url, headers=headers, json=payload)
           
                response = resp.json()

                #if response['detail']:
                print(response)
                refs = Ref.objects.all()
             
                if response['status_code'] == '00':
                    finacle_ref = response['tran_id']

                    for item in refs:
                        if entry.mt103_related_ref.startswith(item.reference):
                            Transactions.objects.filter(mt103_related_ref=entry.mt103_related_ref).update( team=item.team, finacle_ref=finacle_ref, nostro_account=nostro_acct, suspense=suspense, status='success' )
                
                else:
                     for item in refs:
                        if entry.mt103_related_ref.startswith(item.reference):
                            Transactions.objects.filter(mt103_related_ref=entry.mt103_related_ref).update( team=item.team, status='failed' )   
            # else:
            #     return JsonResponse({"status": "no details to process"})
                            
 
    return JsonResponse({"status": "processed"})


    # for entry in get_entries:
    #     if entry.ordering_customer != "":
    #         # Operations
    #         print("Operations")
    #         for acct in accounts:
    #             if entry.currency == acct.currency:

    #                 payload  =  {
    #                             "debit_acct": entry.account_num, # Get Debit account
    #                             "credit_acct": entry.credit_acct,  # Get Credit account
    #                             "tran_amt": entry.debit_amount,   #Clean amount
    #                             "tran_crncy": entry.currency,   
    #                             "tran_particulars": entry.tran_remark,
    #                             "tran_remarks": entry.tran_particular[:20]  # Get Trans Remarks
    #                             }
    #                 resp = requests.request("POST", url, headers=headers, json=payload)
    #                 response = resp.json()

    #     elif entry.ordering_customer == "" and entry.sender_receiever_info == "":
    #         print("Treasury Operations")



    #     elif entry.ordering_customer == "" and entry.sender_receiever_info != "":
    #         print("Trade Finance")





