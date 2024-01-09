
from django.urls import path
from adminapp import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('', views.logoutPage, name='logout'),
    path('add-reference/', views.addreference, name='addreference'),
    path('add-account/', views.addaccount, name='addaccount'),
    path('balance/', views.balances, name='balance'),
    path('dashboard/', views.dashboard, name='dashboard'),

    
    
    path('failedtransactions/', views.failedtransactions, name='failedtransactions'),
    path('dailyfailedtransaction/<str:pk>/', views.dailyfailedtransaction, name='dailyfailedtransaction'),


   
    path('generatemsg/<str:pk>/', views.generatemsg, name='generatemsg'),

    
    path('processed/', views.processedtransactions, name='processed'),
    path('dailyprocessedtransaction/<str:pk>/', views.dailyprocessedtransaction, name='dailyprocessedtransaction'),
    path('unprocessed/', views.unprocessedtransactions, name='unprocessed'),
    path('dailyunprocessedtransaction/<str:pk>/', views.dailyunprocessedtransaction, name='dailyunprocessedtransaction'),
    path('successfulposting/', views.successtransactions, name='successfulposting'),
    path('dailysuccesstransaction/<str:pk>/', views.dailysuccesstransaction, name='dailysuccesstransaction'),

    path('processreference/<str:pk>/', views.processreference, name='processreference'),
    path('searchreference/', views.SearchReference, name='searchreference'),

    path('unassigned/', views.unassigned, name='unassigned'),
    path('dailyunassigned/<str:pk>/', views.dailyunassigned, name='dailyunassigned'),
    
]
