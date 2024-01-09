# Generated by Django 4.1.3 on 2023-09-11 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(blank=True, max_length=50)),
                ('currency', models.CharField(max_length=5)),
                ('account_num', models.CharField(max_length=20)),
                ('suspense', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ref',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=150)),
                ('reference', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100, unique=True)),
                ('senders_ref', models.CharField(max_length=50)),
                ('value_date_and_tran_amount', models.CharField(blank=True, max_length=150, null=True)),
                ('value_date', models.CharField(max_length=20)),
                ('currency', models.CharField(blank=True, max_length=5)),
                ('trans_amount', models.CharField(max_length=100)),
                ('ordering_institution', models.CharField(blank=True, max_length=100)),
                ('mt103_related_ref', models.CharField(max_length=100)),
                ('sender_receiever_info', models.CharField(blank=True, max_length=250)),
                ('ordering_customer', models.CharField(blank=True, max_length=150)),
                ('account_id', models.CharField(max_length=100)),
                ('footer', models.CharField(blank=True, max_length=150)),
                ('message_type', models.CharField(blank=True, max_length=50)),
                ('reciever_bic', models.CharField(blank=True, max_length=100)),
                ('header1', models.CharField(blank=True, max_length=250)),
                ('intermidiary', models.CharField(blank=True, max_length=50)),
                ('finacle_ref', models.CharField(blank=True, max_length=150)),
                ('nostro_account', models.CharField(blank=True, max_length=30)),
                ('suspense', models.CharField(blank=True, max_length=30)),
                ('team', models.CharField(blank=True, max_length=30)),
                ('qm_processed', models.CharField(default='pending', max_length=15)),
                ('status', models.CharField(default='pending', max_length=15)),
                ('entry_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnMatchedTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100, unique=True)),
                ('senders_ref', models.CharField(max_length=50)),
                ('value_date_and_tran_amount', models.CharField(blank=True, max_length=150, null=True)),
                ('value_date', models.CharField(max_length=20)),
                ('currency', models.CharField(blank=True, max_length=5)),
                ('trans_amount', models.CharField(max_length=100)),
                ('ordering_institution', models.CharField(blank=True, max_length=100)),
                ('mt103_related_ref', models.CharField(max_length=100, unique=True)),
                ('sender_receiever_info', models.CharField(blank=True, max_length=250)),
                ('ordering_customer', models.CharField(blank=True, max_length=150)),
                ('account_id', models.CharField(max_length=100)),
                ('footer', models.CharField(blank=True, max_length=150)),
                ('message_type', models.CharField(blank=True, max_length=50)),
                ('reciever_bic', models.CharField(blank=True, max_length=100)),
                ('header1', models.CharField(blank=True, max_length=250)),
                ('intermidiary', models.CharField(blank=True, max_length=50)),
                ('finacle_ref', models.CharField(blank=True, max_length=150)),
                ('nostro_account', models.CharField(blank=True, max_length=30)),
                ('suspense', models.CharField(blank=True, max_length=30)),
                ('team', models.CharField(blank=True, max_length=30)),
                ('qm_processed', models.CharField(default='pending', max_length=15)),
                ('status', models.CharField(default='pending', max_length=15)),
                ('entry_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
            ],
        ),
    ]