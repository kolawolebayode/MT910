
import requests
import json
import oracledb
#import logging
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
from swiftapp.models import Transactions, Ref, Acct
from decouple import config
from django.db import IntegrityError
# from webhook.models import TransactionCallBackInfo
# from core.dbcon import oracle_conn as conn
from datetime import date, datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from swiftapp.queuemanager import oracle_conn_tran_id, qm
from swiftapp.payment import gen_token
oracledb.init_oracle_client()
tran_date = datetime.now().strftime("%Y-%m-%d")


payment_url = config('payment_url')
app_url = config('app_url')
# Create your views here.
#logger = logging.getLogger('django')


# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
   
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome' + ' ' + username.capitalize())
            return redirect('dashboard') 
        else:
            # messages.error(request, 'Incorrect Username/Password entered')
            # return redirect('login')
            return redirect('dashboard') 
    context = {}
    return render(request, "main/login.html", context) 

def login_page2(request):
    if request.method == 'POST':
        email = request.POST["username"]
        password = request.POST["password"]

        
        url = "http://dx.ubauk.com:8009/api/v1/authuser"

        payload = json.dumps({
        "email": email,
        "password": password
        })
        headers = {
        'Content-Type': 'application/json'
        }

        username = email.replace('@ubauk.com', "")
        response = requests.request("POST", url, headers=headers, data=payload)     
        resp = response.json()
       
        if resp['status']== 'success': 
            # Create user and save to the database
            try:
                user = User.objects.create_user(username, email, 'myadminreport')

            except IntegrityError:
                pass
            user = authenticate(request, username=username, password='myadminreport')
 
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome' + ' ' + username.capitalize())
                return redirect('dashboard') 
        else:
            messages.error(request, 'Incorrect Username/Password')
            return redirect('login')

    context = {}
    return render(request, "main/login.html", context) 



@login_required(login_url  ='login')
def logoutPage(request):
    logout(request)
    return redirect('login')



# @login_required(login_url  ='login')
def dashboard(request):

    sucessful_posted_trans_count =  Transactions.objects.filter(status='success').count()
    #processed_trans_count =  Transactions.objects.filter(status='success', qm_processed='complete').count()
    processed_trans_count =  Transactions.objects.filter(status='success', qm_processed='pending').count()
    unprocessed_trans_count =  Transactions.objects.filter(status='pending', team='Trade Operations').count()
    #unprocessed_trans_count =  Transactions.objects.filter(status='success', qm_processed='unprocessed').count() #look at test this is for stage 2 i changed bcos of the posting issue
    failed_posted_trans_count =  Transactions.objects.filter(status='failed').count()
    context = {"sucessful_posted_trans_count":sucessful_posted_trans_count, "processed_trans_count":processed_trans_count, "failed_posted_trans_count":failed_posted_trans_count, "unprocessed_trans_count":unprocessed_trans_count}
    return render(request, "main/dashboard.html", context)


# @login_required(login_url  ='login')
def addreference(request):
    references =  Ref.objects.all()
        
    if request.method == 'POST':
        reference =  request.POST.get('reference')
        team =  request.POST.get('team')

        url = f"{app_url}/api/reference"
        print(url)
        print(reference)
        print(team)
        payload = json.dumps({
                            "team": team,
                            "reference": reference
                            })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        #print(response.text)
        if response.status_code == 200 or response.status_code == 201:
            #logger.info(f"Reference {reference} has been added successfully")
            messages.success(request, f"Reference {reference} has been added successfully")
            return redirect('addreference')
        else:
            #logger.error(f"Error! {reference} already exists")
            messages.error(request, f"Error! {reference} already exists")
            return redirect('addreference')
    
    context = {"references":references}
    return render(request, "main/reference.html", context)



def addaccount(request):
    accts =  Acct.objects.all()
    
    references = Ref.objects.all()    
    if request.method == 'POST':
        currency =  request.POST.get('currency')
        account_num =  request.POST.get('account_num')
        sender =  request.POST.get('sender')
        suspense =  request.POST.get('suspense')

        url = f"{app_url}/api/accounts"
  
        payload = json.dumps({
                            "account_num": account_num,
                            "currency": currency,
                            "sender": sender,
                            "suspense": suspense
                            })
        headers = {
        'Content-Type': 'application/json'
        }
     
        response = requests.request("POST", url, headers=headers, data=payload)
        
        if response.status_code == 200 or response.status_code == 201:
            messages.success(request, f"Reference {account_num} has been added successfully")
            return redirect('addaccount')
        else:
            messages.error(request, f"Error: Try again")
            return redirect('addaccount')
    
    context = {"references":references, "accts":accts}
    return render(request, "main/accounts.html", context)



def balances(request):
    fi_un = config('fi_un')
    fi_pw = config('fi_pw')
    fi_cs = config('fi_cs')
    accts =  Acct.objects.all().distinct('suspense')
    try:
        connection = oracledb.connect(user= fi_un, password=fi_pw, dsn= fi_cs) 
        print("connected")
        balances_resp = []
        try:
            with connection.cursor() as cursor:
                
                for acct in accts:
               
                    bal_sql = f"select FORACID, CLR_BAL_AMT from tbaadm.GAM WHERE FORACID  = '{acct.suspense}'"
                    get = cursor.execute(bal_sql)
                    items = get.fetchone() 
                    
                    balances_resp.append(f"{items[0]}  -  {items[1]}")

        except Exception as e:
            print(e)
            balances_resp = []
            pass
        finally:
            cursor.close
    except Exception as e:
        messages.error(request, f'Error connecting to Finacle, Try Again! ')
        return redirect('balance')
        
    context = { "accts":accts, "balances_resp":balances_resp}
    return render(request, "main/balance.html", context)




# @login_required(login_url  ='login')
#Success Posting in Finacle and processing in TI
def processedtransactions(request): 
    trans_list =  Transactions.objects.filter(status='success', qm_processed='pending').values('entry_date').annotate(count=Count('id')).order_by('-entry_date').distinct()
    context = {"trans_list":trans_list}
    return render(request, "main/processedtransactioncount.html", context)

def dailyprocessedtransaction(request, pk):
    trans_list = Transactions.objects.filter(entry_date = pk, status='success', qm_processed='pending').order_by('-id')
    context = {"trans_list":trans_list}
    return render(request, "main/dailyprocessedtransactions.html", context)

def unprocessedtransactions(request): 
    #trans_list =  Transactions.objects.filter(status='pending', qm_processed='pending').values('entry_date').annotate(count=Count('id')).order_by('-entry_date').distinct()
    trans_list =  Transactions.objects.filter(status='pending', team='Trade Operations').values('entry_date').annotate(count=Count('id')).order_by('-entry_date').distinct()

    context = {"trans_list":trans_list}
    return render(request, "main/unprocessedtransactioncount.html", context)

def dailyunprocessedtransaction(request, pk):
    #trans_list = Transactions.objects.filter(entry_date = pk, status='pending', qm_processed='pending').order_by('-id')
    trans_list = Transactions.objects.filter(entry_date = pk, status='pending', team='Trade Operations').order_by('-id')
    context = {"trans_list":trans_list}
    return render(request, "main/dailyunprocessedtransactions.html", context)

# Success Posting in Finacle only
def successtransactions(request): 
    trans_list =  Transactions.objects.filter(status='success' ).values('entry_date').annotate(count=Count('id')).order_by('-entry_date').distinct()
    context = {"trans_list":trans_list}
    return render(request, "main/successtransactioncount.html", context)


def dailysuccesstransaction(request, pk):
    trans_list = Transactions.objects.filter(entry_date = pk, status='success').order_by('-id')
   
    context = {"trans_list":trans_list}
    return render(request, "main/dailysuccesstransactions.html", context)


def failedtransactions(request): 
    trans_list =  Transactions.objects.filter(status='failed').values('entry_date').annotate(count=Count('id')).order_by('-entry_date').distinct()

    context = {"trans_list":trans_list}
    return render(request, "main/failedtransactioncount.html", context)


def dailyfailedtransaction(request, pk):
    trans_list = Transactions.objects.filter(entry_date = pk, status='failed').order_by('-id')
   
    context = {"trans_list":trans_list}
    return render(request, "main/dailyfailedtransactions.html", context)


def generatemsg(request, pk):
    trans_list = Transactions.objects.filter(id=pk)
    #with open('readme.txt', 'w') as f:
    for item in trans_list:
        response = HttpResponse(content_type ='text/plain') 
        response['Content-Disposition'] = f"attachment; filename={item.file_name}"  
        line1 = item.header1
        line2 = f":20:{item.senders_ref}"
        line3 = f":21:{item.mt103_related_ref}"
        line4 = f":25:{item.account_id}"
        line5 = f":32A:{item.value_date_and_tran_amount}"
        line6 = f":52A:{item.ordering_institution}"
        line7 = f":56A:{item.intermidiary}"
        line8 = f":72:{item.sender_receiever_info}"
        line9 = item.footer
            
        lines = [ line1 + "\n",  line2 + "\n",line3 + "\n",line4 + "\n",line5 + "\n",
                    line6 + "\n",line7 + "\n",line8 + "\n", line9 ]
        response.writelines(lines)
        return response
    pass


def SearchReference(request):
    if request.method == 'POST':
        reference = request.POST.get('reference')
        Transactions.objects.filter( id = pk).update(qm_processed = 'complete')
        trans_list = Transactions.objects.filter(mt103_related_ref = reference, status='success', qm_processed='unprocessed').order_by('-id')

        context = {"trans_list":trans_list}
        return render(request, "main/dailyunprocessedtransactions.html", context)

    context = {}
    return render(request, "main/ref_search.html", context)



def unassigned(request): 
    trans_list =  Transactions.objects.filter(team='unsorted' ).values('entry_date').annotate(count=Count('id')).order_by('-entry_date').distinct()
    context = {"trans_list":trans_list}
    return render(request, "main/unassigned.html", context)


def dailyunassigned(request, pk):
    trans_list = Transactions.objects.filter(team='unsorted' ).order_by('-id')
   
    context = {"trans_list":trans_list}
    return render(request, "main/dailyunassigned.html", context)


# Fetch reference for unprocessed transactions and push to XML
def processreference(request, pk):
    un = config('un')
    pw = config('pw')
    cs = config('cs')
    ref = Transactions.objects.get(id=pk)
    try:
        connection = oracledb.connect(user= un, password=pw, dsn= cs) 
        print("connected")
        try:
            with connection.cursor() as cursor:
                
               # reference = ref.mt103_related_ref
                reference = 'ILCITF-20-01374'

                sql = ("""select trim(m.master_ref) as "Master", trim(ex.code79) as "Product"
                            from master m
                                left join exempl30 ex on m.exemplar = ex.key97
                                where m.pri_ref = '%s' and m.status = 'LIV' """%(reference)
                       )
                get = cursor.execute(sql)
                items = get.fetchall() 

    # print(sql)
        except Exception as e:
            pass
        finally:
            cursor.close

        if request.method == 'POST':
            unprocessed_ref = request.POST.get("master_ref")

            master_ref, product = unprocessed_ref.split(",")
            master_ref = master_ref.replace("('", "")
            master_ref = master_ref.replace("'", "")
            product = product.replace("')", "")
            product = product.replace("'", "")
            product = product.strip()
            master_ref= master_ref.strip()
            reference = (ref.mt103_related_ref)
    
            trans_list = Transactions.objects.filter(id=pk, status = 'success', qm_processed = 'unprocessed')
            for data in trans_list:
                if product == 'FSA':
                   
                #Send this to the  TO TI XML
                    message = (f"""<?xml version="1.0" standalone="yes"?><ServiceRequest xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:m='urn:messages.service.ti.apps.tiplus2.misys.com' xmlns:c='urn:common.service.ti.apps.tiplus2.misys.com' xmlns='urn:control.services.tiplus2.misys.com'>
<RequestHeader>
<Service>TI</Service>
<Operation>TFFSARPY</Operation>
<Credentials>
<Name>SUPERVISOR</Name>
<Password>Password</Password>            
</Credentials>
<ReplyFormat>FULL</ReplyFormat>
<NoRepair>N</NoRepair>
<NoOverride>N</NoOverride>
<CorrelationId></CorrelationId>
<TransactionControl>NONE</TransactionControl>
</RequestHeader>
<m:TFFSARPY>
<m:Context>
<c:Branch>LOND</c:Branch>            
<c:Customer>{data.ordering_institution}</c:Customer>
<c:CustomerSwiftAddress>{(data.ordering_customer)}</c:CustomerSwiftAddress>
<c:Product>FSA</c:Product>
<c:Event>RFS</c:Event>
<c:OurReference>{master_ref}</c:OurReference>
<c:TheirReference>ILCITF-20-01204</c:TheirReference>
<c:Team>Hub</c:Team>            
</m:Context>            
<m:MasterRef>{master_ref}</m:MasterRef>        
<m:RepaymentAction>O</m:RepaymentAction>
<m:RepaymentReference>{data.senders_ref}</m:RepaymentReference>   
<m:ValueDate>{data.value_date}</m:ValueDate>
<m:PrincipalRepaymentAmount>
<c:Amount>{data.trans_amount}</c:Amount>
<c:Currency>{data.currency}</c:Currency>
</m:PrincipalRepaymentAmount>
<m:AdditionalData>
<c:DataItem>
<c:Name>Extra</c:Name>
<c:Value>{data.sender_receiever_info}</c:Value>
</c:DataItem>
</m:AdditionalData>        
</m:TFFSARPY>
</ServiceRequest>
""") 

                    #print(message)
                    
                    qm(message)  
                    Transactions.objects.filter( id = pk).update(qm_processed = 'complete')
                    messages.success(request, f'Processed SUccessfully')
                    return redirect('dailyunprocessedtransaction' , data.entry_date)
                
                #What to do with other products
                elif product != 'FSA':
                    messages.error(request, f'please check product {product}')
                    return redirect('dailyunprocessedtransaction' , data.entry_date)

    except Exception as e:
        messages.error(request, f'{e}')
        return redirect('dailyunprocessedtransaction' , ref.entry_date)
    context = {"items":items, 'ref':ref}
    return render(request, "main/process_ref.html", context)
    