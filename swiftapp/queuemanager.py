import logging
import oracledb
import os
#import pymqi
from decouple import config
from django.http import HttpResponse, JsonResponse
from datetime import date, datetime
from .models import Transactions


#oracledb.init_oracle_client(lib_dir=r"C:\instantclient_21_9")
oracledb.init_oracle_client()

def qm(message):
    queue_manager = config('queue_manager')
    channel = config('channel')
    host = config('host')
    port = config('port')
    queue_name = config('queue_name')
    conn_info = '%s(%s)' % (host, port)

    #qmgr = pymqi.connect(queue_manager, channel, conn_info)

    try:
        qmgr = pymqi.connect(queue_manager, channel, conn_info)
    except pymqi.MQMIError as e:
        if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_HOST_NOT_AVAILABLE:
            print('Such a host `%s` does not exist.' % host)
            #logging.error('Such a host `%s` does not exist.' % host)
    queue = pymqi.Queue(qmgr, queue_name)
    #msg = queue.get()
    msg = queue.put(message)
    #msg = queue.get()
    queue.close()
    qmgr.disconnect()

    return queue




def oracle_conn_tran_id(reference):
    un = config('un')
    pw = config('pw')
    cs = config('cs')

    try:
        connection = oracledb.connect(user= un, password=pw, dsn= cs) 
        try:
            with connection.cursor() as cursor:
               # print(cursor)

                tran_date = datetime.now().strftime("%d-%b-%Y")
                
                # Check if the LC Reference is find a multiple match in TI
                sql = ("""
                        select trim(m.master_ref) master_ref , trim(m.refno_pfix) refno_pfix, trim(m.pri_ref)pri_ref
                        from master m
                            left join (
                                select pri_ref, count(pri_ref) as Count
                                    from master
                                        where status = 'LIV' and pri_ref <> ' '
                                            group by pri_ref
                            ) mc on m.pri_ref = mc.pri_ref
                                where mc.Count = '1' and m.status = 'LIV' and m.refno_pfix = 'FSA'
                        and m.pri_ref = '%s' """ %(reference)
                        )
                get = cursor.execute(sql)
                qs = get.fetchone() 
                
                


                #FETCH DATA FROM TRANSACTION DB TO PASS TO XML
                trans_list = Transactions.objects.filter(status = 'success', qm_processed = 'pending')


                if not trans_list:
                    return JsonResponse({'status': "no data"})
           
                for data in trans_list:

                # If multiiple match is found  from sql query above save to DB and end
                    if qs is None:
        
                        Transactions.objects.filter( id = data.id).update(qm_processed = 'unprocessed')
                        return  JsonResponse({'error': 'Multiple match found'})



                    #PREPARE XML HERE
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
<c:Product>{qs[1]}</c:Product>
<c:Event>RFS</c:Event>
<c:OurReference>EXP/20/03376</c:OurReference>
<c:TheirReference>ILCITF-20-01204</c:TheirReference>
<c:Team>Hub</c:Team>            
</m:Context>            
<m:MasterRef>EXP/20/03376</m:MasterRef>        
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
                    #qm(message)
                
                    Transactions.objects.filter( id = data.id).update(qm_processed = 'complete')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': e})
        finally:
            cursor.close
    except Exception as e:
        return JsonResponse({'error': e})
    


#ILCITF-20-01051
#                     message = (f"""<?xml version="1.0" standalone="yes"?><ServiceRequest xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:m='urn:messages.service.ti.apps.tiplus2.misys.com' xmlns:c='urn:common.service.ti.apps.tiplus2.misys.com' xmlns='urn:control.services.tiplus2.misys.com'>
# <RequestHeader>
# <Service>TI</Service>
# <Operation>TFFSARPY</Operation>
# <Credentials>
# <Name>SUPERVISOR</Name>
# <Password>Password</Password>            
# </Credentials>
# <ReplyFormat>FULL</ReplyFormat>
# <NoRepair>N</NoRepair>
# <NoOverride>N</NoOverride>
# <CorrelationId></CorrelationId>
# <TransactionControl>NONE</TransactionControl>
# </RequestHeader>
# <m:TFFSARPY>
# <m:Context>
# <c:Branch>LOND</c:Branch>            
# <c:Customer>{data.ordering_institution}</c:Customer>
# <c:CustomerSwiftAddress>{(str(data.ordering_institution) + 'XXX')}</c:CustomerSwiftAddress>
# <c:Product>{qs[1]} </c:Product>
# <c:Event>RFS</c:Event>
# <c:OurReference>{qs[0]}</c:OurReference>
# <c:TheirReference>{qs[2]}</c:TheirReference>
# <c:Team>Hub</c:Team>            
# </m:Context>            
# <m:MasterRef>{qs[0]}</m:MasterRef>        
# <m:RepaymentAction>O</m:RepaymentAction>
# <m:RepaymentReference>789</m:RepaymentReference>                
# <m:PrincipalRepaymentAmount>
# <c:Amount>{data.trans_amount}</c:Amount>
# <c:Currency>{data.currency}</c:Currency>
# </m:PrincipalRepaymentAmount>
# <m:AdditionalData>
# <c:DataItem>
# <c:Name>Extra</c:Name>
# <c:Value>/BNF/BNG INTEREST FEE ON SUBJECT
# //LOAN PAYMENT. SOME NEW MESSAGE
# //EXP/55/07012</c:Value>
# </c:DataItem>
# </m:AdditionalData>        
# </m:TFFSARPY>
# </ServiceRequest>
# """) 
