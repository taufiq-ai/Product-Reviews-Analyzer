from django.shortcuts import render, redirect
from django.http import HttpResponse

#To query in Database MODEL
from .models import *

#To manage POST forms
from .forms import OrderForm, CreateUserForm, MyForm

# login essentials
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate, login, logout
from django.contrib import messages

#Decorators for Role based permission
from .decorators import unauthenticated_user, allowed_users

#Managing Database User group
from django.contrib.auth.models import Group

""" Create your views here. """

#1. Registration
from django.contrib.auth.forms import UserCreationForm
@unauthenticated_user #Logged in User can't go to register page
def registration(request):     
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name = 'client') #Fetch client group 
            user.groups.add(group) #Add newly registered user into client group
            
            Client.objects.create(
                user = user,     #user automatically added to client model
            )
            return redirect('/login/')
    context = {'form':form}
    return render(request, "SentimentAnalyzer/register.html", context)




#Login
@unauthenticated_user #Logged in User can't go to Login page
def login_page(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Check Usename or Password")
            return render(request, "SentimentAnalyzer/login.html", context)
    return render(request, "SentimentAnalyzer/login.html", context)




#Logout
def logoutUser(request):
    logout(request)
    return redirect('/login/')




def home(request):
    context = {}
    return render(request, "SentimentAnalyzer/index.html", context)



# UPLOADATION analyze_review - Rownok
@login_required(login_url='login') #The decorator force user to login to view this template
def review(request):
    saved = False
    if request.method == "POST":
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            # file = File()
            # file.name = MyForm.cleaned_data["filename"]
            # file.file = MyForm.cleaned_data["file"]
            saved = True
            file_ = form.save()            
            return redirect('/dashboard/')
    else:
        form = MyForm()
    context = {'form': form}
    return render(request, 'SentimentAnalyzer/review.html', context)

# DASHBOARD - User's order details 
@login_required(login_url='login') #The decorator force user to login to view this template
@allowed_users(allowed_roles=['client'])
def userPage(request):

    #order model for dashboard
    orders = request.user.client.order_set.all()
    total_order = orders.count()
    analyzed = orders.filter(status='Analyzed').count()
    pending = orders.filter(status='Pending').count()

    #File model
    files = request.user.client.file_set.all()
    totalfile = files.count() #working
    # filename = files.prefetch_related('filename')

    # filename = files.filename

    context = {'orders':orders, 'total_order':total_order,'pending':pending,'analyzed':analyzed, 'files':files} #'totalfile':totalfile, 'filename':filename 
    return render(request,"SentimentAnalyzer/dashboard.html", context)



##########              Admin  Panel Views             ##### 
#      (Admin Panel, Client info, File Storage, Order creation ) #


@allowed_users(allowed_roles=['admin'])
def adminpanel(request):
    orders = Order.objects.all() #fetch all order objects(fileds)
    clients = Client.objects.all() #fetch all client objects
    total_client = clients.count() #count total client objects 
    total_order = orders.count() #count total orders
    analyzed = orders.filter(status='Analyzed').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'clients':clients, 'total_order': total_order, 'analyzed':analyzed,'pending':pending}
    return render(request,'SentimentAnalyzer/adminpanel.html', context)



@allowed_users(allowed_roles=['admin'])
def client(request,pk_test):
    client = Client.objects.get(id = pk_test) #Fetch client according to Primary Key
    pk_client_orders = client.order_set.all() # fetched client's orders are stored
    total_order = pk_client_orders.count()
    context = {'client':client,'pk_client_orders':pk_client_orders,'total_order':total_order}
    return render(request, "SentimentAnalyzer/client.html", context)



@allowed_users(allowed_roles=['admin'])
def files(request):
    files = File.objects.all() #files var storing All objects of File model
    context = {'files':files}
    return render(request, "SentimentAnalyzer/files.html", context)



# from .forms import OrderForm
@allowed_users(allowed_roles=['admin'])
def createorder(request):
    form = OrderForm
    if request.method == 'POST':
        # print('printing POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/adminpanel')
    context = {'form':form}
    return render(request,"SentimentAnalyzer/order_form.html", context)

