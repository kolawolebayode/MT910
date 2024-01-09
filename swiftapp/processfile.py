#import pysftp
from datetime import datetime

# Handle the processing mt910 message.. all logic to clean up file
def fileprocessor(output, sender_info):
 
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
            

    return {"all_data":all_data, "mt103_related_ref":mt103_related_ref}