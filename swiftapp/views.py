#import schedule
import time
#from schedule import repeat, every
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse

from rest_framework.generics import ListCreateAPIView
from .serializers import REFSerializer, ACCTSerializer
from .models import Ref, Acct
from .services import readfile
from .payment import Payment
from .queuemanager import oracle_conn_tran_id, qm
#import pysftp
import paramiko

# Create your views here.
def fileprocess(requests):
    response = readfile()
    #read_folder()
    print(response)
    return HttpResponse(response)


class REFView(ListCreateAPIView):
    queryset = Ref.objects.all()
    serializer_class = REFSerializer



class ACCOUNTView(ListCreateAPIView):
    queryset = Acct.objects.all()
    serializer_class = ACCTSerializer


def queuemanager(requests):
    y = qm()
    print(y)
    return HttpResponse(y)    

#Use for processing and payment
def Processing(requests):
    #return
    readfile()
    return Payment()
    

def PustToTi(requests):
    reference ='ILCUNC-20-00359'
    master_ref =""
    ref_id = ""
    response = oracle_conn_tran_id(reference, master_ref, ref_id)

    return response



