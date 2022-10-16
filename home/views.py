from urllib import response
from django.http import HttpResponseServerError
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from home.models import Contact
from bs4 import BeautifulSoup

import requests

 


from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import CreateUserForm
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form=CreateUserForm()
        if request.method == 'POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user =  form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+user)

                return redirect('login')

    context={'form':form}
    return render(request,'register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                    messages.info(request, 'Username OR password is incorrect')
                    
        context={}
        return render(request,'login.html',context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def index(request):
    a ="cipla"
  
    url="https://www.screener.in/company/"+a
    req = requests.get(url)

    soup=BeautifulSoup(req.content,'html.parser')
    sp=soup.find_all('span')[1]
    price =str(sp.string)
    mg= price.replace("₹ ","")
    request.session['mg']=mg
    request.session['a']=a

    return render(request,'index.html',{'mg':mg, 'name_st':a})
    

@login_required(login_url='login')
def about(request):
    return render(request,'about.html')

@login_required(login_url='login')
def services(request):
    return render(request,'services.html')

@login_required(login_url='login')
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'contact.html')
    

@login_required(login_url='login')
def stocks(request):
    return render(request, 'stocks.html')


@login_required(login_url='login')
def getprice(request):
    
    if request.method =="POST":
       a =request.POST.get('name')
       url="https://www.screener.in/company/"+a
       req = requests.get(url)

       soup=BeautifulSoup(req.content,'html.parser')
       sp=soup.find_all('span')[1]
       price =str(sp.string)
       mg= price.replace("₹ ","")
       request.session['mg']=mg
       request.session['a']=a


       return render(request,'getprice.html',{'mg':mg, 'name_st':a})
def info(request):
    if request.method=="POST":
        ip =request.POST.get('input')
        dt=request.POST.get('date')
        r=request.get('https://api.polygon.io/v3/refernce/tickers/'+ip+'?date='+dt+'&apikey=')

