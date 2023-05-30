from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name='home'),
    path('login-h/', loginpage, name="login-h"),
    path('register/', register, name="register"),
    path('logout-h/', logoutUser, name="logout-h"),
    path('add/',add_patient,name='add'),
    path('image/',imagefusion,name="image-fusion"),
    path('merge/',merge,name='merge'),
    path('brain_merge/',brain_merge,name='brain_merge'),
    path('lung_merge/',lung_merge,name='lung_merge'),
    path('home/',home,name='home'),
    path('history/',history,name='history'),
    path('department/',department,name='department'),
    path('heart/',heart,name='heart'),
    path('liver/',liver,name='liver'),
    path('diabetics/', diabetics, name='diabetics'),
    path('heart_disease/',heart_disease,name='heart_disease'),
    path('liver_disease/',liver_disease,name='liver_disease'),
    path('diabetics_disease/',diabetics_disease,name='diabetics_disease'),
    path('addmore/', addmore, name='addmore'),
    path('upload/', upload, name='upload'),
    path('details',details,name='details'),
    #path('merge_datas/',merge_datas,name='merge_datas'),
    path('det/',det,name='det'),
    path('det1/',det1,name='det1'),
    path('hisdata/',hisdata,name='hisdata'),
    path('merge_data/',merge_data,name='merge_data'),
]


'''
    
    path('data/',data,name='data'),
    path('pre-processing/',preprocessing,name='pre-processing'),
    path('datamerge/',datamerge,name='datamerge'),
    
    path('database/',database,name='database'),
    ,
    ,
    
    path('details',details,name='details'),
    path('merge_datas/',merge_datas,name='merge_datas'),
    path('home/',home,name='home'),'''