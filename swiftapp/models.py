from django.db import models

# Create your models here.
class Transactions(models.Model):
    file_name = models.CharField(max_length=100, unique=True)
    senders_ref = models.CharField(max_length=150)
    value_date_and_tran_amount = models.CharField(max_length=150, null=True, blank=True)
    value_date = models.CharField(max_length=120)
    currency = models.CharField(max_length=50, blank=True)
    trans_amount = models.CharField(max_length=100)
    ordering_institution = models.CharField(max_length=100, blank=True)
    mt103_related_ref = models.CharField(max_length=100)
    sender_receiever_info = models.CharField(max_length=250, blank=True)
    ordering_customer = models.CharField(max_length=150, blank=True)
    account_id  = models.CharField(max_length=100)
    footer = models.CharField(max_length=150, blank=True)
    message_type = models.CharField(max_length=150, blank=True)
    reciever_bic = models.CharField(max_length=100, blank=True)
    header1 = models.CharField(max_length=250, blank=True)
    team = models.CharField(max_length=150, blank=True)
    intermidiary = models.CharField(max_length=150, blank=True, null=True)
    finacle_ref = models.CharField(max_length=150, blank=True)
    nostro_account = models.CharField(max_length=130, blank=True)
    suspense = models.CharField(max_length=130, blank=True)
    team = models.CharField(max_length=130, blank=True)
    qm_processed = models.CharField( max_length=150, default='pending')
    status = models.CharField( max_length=150, default='pending')
    entry_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)


class Ref(models.Model):
    team = models.CharField(max_length=150)
    reference = models.CharField(max_length=150)


class Acct(models.Model):
    sender = models.CharField(max_length=50, blank=True)
    currency = models.CharField(max_length=50)
    account_num = models.CharField(max_length=50)
    suspense = models.CharField(max_length=50)

    

class UnMatchedTransaction(models.Model):
    file_name = models.CharField(max_length=100, unique=True)
    senders_ref = models.CharField(max_length=50)
    value_date_and_tran_amount = models.CharField(max_length=150, null=True, blank=True)
    value_date = models.CharField(max_length=50)
    currency = models.CharField(max_length=5, blank=True)
    trans_amount = models.CharField(max_length=100)
    ordering_institution = models.CharField(max_length=100, blank=True, null=True)
    mt103_related_ref = models.CharField(max_length=100, unique=True)
    sender_receiever_info = models.CharField(max_length=250, blank=True)
    ordering_customer = models.CharField(max_length=150, blank=True)
    account_id  = models.CharField(max_length=100)
    footer = models.CharField(max_length=150, blank=True)
    message_type = models.CharField(max_length=150, blank=True)
    reciever_bic = models.CharField(max_length=100, blank=True)
    header1 = models.CharField(max_length=250, blank=True)
    team = models.CharField(max_length=150, blank=True)
    intermidiary = models.CharField(max_length=50, blank=True)
    finacle_ref = models.CharField(max_length=150, blank=True)
    nostro_account = models.CharField(max_length=50, blank=True)
    suspense = models.CharField(max_length=50, blank=True)
    team = models.CharField(max_length=50, blank=True)
    qm_processed = models.CharField( max_length=50, default='pending')
    status = models.CharField( max_length=50, default='pending')
    entry_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)


