from django.urls import path, include
from classifier_app import views
from django.conf.urls import url


urlpatterns = [
    url('^$',views.index,name='homepage'),
    url('predictImage',views.predictImage,name='predictImage'),
    url('viewDataBase',views.viewDataBase,name='viewDataBase'),
    ]

