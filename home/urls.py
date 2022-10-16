from django.contrib import admin
from django.urls import path,include 
from home import views


urlpatterns = [

    path("register",views.registerPage,name='regsiter'),

    path("login",views.loginPage,name='login'),
    
    path("logout",views.logoutUser,name='logout'),
    
    path("",views.index,name='home'),
    
    path("about",views.about,name='about'),
    
    path("services",views.services,name='services'),
    
    path("contact",views.contact,name='contact'),

    path("stocks",views.stocks,name="stocks"),

    path("getprice",views.getprice,name="getprice"),

   
    
]