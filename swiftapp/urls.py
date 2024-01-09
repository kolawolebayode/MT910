"""swiftproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from swiftapp import views
from .views import REFView, ACCOUNTView

urlpatterns = [
    path('fileprocess', views.fileprocess, name='fileprocess'),   
    path('reference', REFView.as_view(), name='ref'),
    path('accounts', ACCOUNTView.as_view(), name='acct'), 
    #path('file_read', views.file_read, name='file_read')
    path('processing', views.Processing, name='processing'),
    path('push_ti', views.PustToTi, name='push_ti'),
    path('queuemanager', views.queuemanager, name='queuemanager'),
    
]
