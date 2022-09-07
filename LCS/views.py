from django.contrib.auth.models import User
from django.core.checks import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import CreateNewUser, CustomerForm
from plotly.offline import plot
import plotly.express as px
import pandas as pd
from .models import *

cart = ''

def signup(request):
    success_message = ''
    if request.method == "POST":
        form = CreateNewUser(request.POST)
        if form.is_valid():
            form.save()
            success_message = "User Created Successfully!"
            return redirect('login')
    else:
        form = CreateNewUser()
    return render(request, "LCS/signup.html", {'form': form, 'success_message': success_message})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if username == 'manager':
                return redirect('ManagerView')
            elif user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'LCS/login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


def home(request):
    products = Product.objects.all()
    customer = customer_data(request)
    cart = Cart(request)
    cart.clear()
    return render(request, 'LCS/dashboard.html', {'products': products, 'customer': customer})

def cart(request):
      template = get_template('LCS/cart.html')
      source = Location.objects.all()
      vehicle = Vehicle.objects.all()
      cart_data = request.session.get('cart')
      total=0
      product_list = list(cart_data.values())
      for x in product_list:
          total += int(x['price'])
      return render(request,'LCS/cart.html',{'source':source,'cart_data':total,'vehicle':vehicle})

def addrecord(request):
      first_name = request.POST['first']
      last_name = request.POST['last']
      mobile = request.POST['mobile']
      email_address = request.POST['email']
      address = request.POST['address']
      member = Customer(first_name=first_name, last_name=last_name, mobile=mobile, email_address=email_address,address=address)
      member.save()
      cart_data = request.session.get('cart')
      product_list = list(cart_data.values())
      source_id = request.POST['source']
      source_city = Location.objects.filter(id=source_id).values('source')
      vehicle = request.POST['vehicle']
      for item in product_list:
            product_id = Product.objects.filter(name=item['name']).values('id')
            cust_id = Customer.objects.filter(email_address=email_address).values('id')
            item_order = Pack.objects.create(
              user_id=cust_id[0]['id'],
              prod_id= product_id[0]['id'],
              ordered=True,
                vehicle_id = vehicle,
                source = source_id
            )
      #return HttpResponseRedirect(reverse('cart'))
      return redirect('OrderSuccessful')

def OrderSuccessful(request):
    return render(request,'LCS/OrderSuccessful.html')


def customer_data(request):
    if request.method == "POST":
        customer = CustomerForm(request.POST)
        if customer.is_valid():
            customer.save()
    else:
        customer = CustomerForm()

    return customer


def pack(request):
    products = Product.objects.all()
    customer = customer_data(request)
    cart = Cart(request)
    return render(request, 'LCS/dashboard.html', {'products': products, 'cart': cart, 'customer': customer})


def cart_add(request, id):

    cart = Cart(request)
    customer = customer_data(request)
    products = Product.objects.all()
    product = Product.objects.get(id=id)

    cart.add(product=product)
    return render(request, 'LCS/dashboard.html', {'products': products, 'cart': cart, 'customer': customer})


def item_clear(request, id):
    cart = Cart(request)
    customer = customer_data(request)
    products = Product.objects.all()
    product = Product.objects.get(id=id)
    cart.remove(product)
    return render(request, 'LCS/dashboard.html', {'products': products, 'cart': cart, 'customer': customer})


def item_increment(request, id):
    products = Product.objects.all()
    cart = Cart(request)
    customer = customer_data(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return render(request, 'LCS/dashboard.html', {'products': products, 'cart': cart, 'customer': customer})


def item_decrement(request, id):
    products = Product.objects.all()
    cart = Cart(request)
    customer = customer_data(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return render(request, 'LCS/dashboard.html', {'products': products, 'cart': cart, 'customer': customer})


def cart_clear(request):
    products = Product.objects.all()
    cart = Cart(request)
    customer = customer_data(request)
    cart.clear()
    return render(request, 'LCS/dashboard.html', {'products': products, 'cart': cart, 'customer': customer})


def get_total(request, id=1):
    cart = Cart(request)
    products = Product.objects.all()
    product = Product.objects.get(id=id)

def ManagerView(request):
    packs = Pack.objects.all()
    products = Product.objects.all()
    vehicles = Vehicle.objects.all()
    packs_data = [
    {
    'User': x.user_id,
    'Product': x.prod_id,
    'OrderDate' : x.ordered_date,
    'Ordered': x.ordered,
    'Vehicle': x.vehicle_id,
    'Source':x.source,
    'Count':x.COUNT
    } for x in Pack.objects.raw('Select *, Count(ordered_date) AS "COUNT" from LCS_pack group by ordered_date')
    ]

    df = pd.DataFrame(packs_data)
    fig = px.line(df, x='OrderDate', y="Count", title = "Number of orders placed for a period of time")
    plt_div = plot(fig, output_type='div', include_plotlyjs=False)


    packs_prod_data = [
    {
    'PackID': p.id,
    'ProductID': p.prod_id,
    'OrderDate' : p.ordered_date,
    'Name':p.name
    } for p in Pack.objects.raw('Select p.id, p.prod_id, p.ordered_date, pr.name from LCS_pack p inner join LCS_product pr on p.prod_id = pr.id')
    ]
    df1 = pd.DataFrame(packs_prod_data)
    # print(df1.Name)
    fig = px.histogram(df1, x="Name", title='Total number of orders per product')
    plt1_div = plot(fig, output_type='div', include_plotlyjs=False)


    packs_vehicle_data = [
    {
    'PackID': v.id,
    'VehicleID': v.vehicle_id,
    'OrderDate' : v.ordered_date,
    'Name':v.name,
    'Count':v.COUNT
    } for v in Pack.objects.raw('Select p.id, p.vehicle_id, p.ordered_date, v.name, count(p.vehicle_id) AS "COUNT" from LCS_pack p inner join LCS_vehicle v on p.vehicle_id = v.id group by p.vehicle_id;')
    ]
    df2 = pd.DataFrame(packs_vehicle_data)
    fig = px.pie(df2, values ="Count", names="Name", title='Total percentage of different modes of transportation')
    plt2_div = plot(fig, output_type='div', include_plotlyjs=False)


    return render(request,'LCS/ManagerView.html', context={ 'plt_div':plt_div, 'plt1_div':plt1_div, 'plt2_div':plt2_div})
