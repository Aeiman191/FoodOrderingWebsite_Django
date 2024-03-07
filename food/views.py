
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm,UserProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile , Restaurant , Products, shippingAddress,order,cart
from django.http import JsonResponse
import json
import datetime
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from geopy.distance import  great_circle



@csrf_exempt
def index(request):
    return render(request,'index.html')



@csrf_exempt
def register(request):
    if request.method=="POST":
        form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f'Your account has been created. You can log in now!')    
            return redirect('/Log-In')
    else:
        form = UserRegistrationForm()
        profile_form = UserProfileForm()

    context = {'form':form,'profile_form':profile_form}
    return render(request,'Signup.html',context)






def logout_request(request):
    messages.info(request, "Logged out successfully!")
    return redirect("/")




def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/order')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "LogIn.html",
                    context={"form":form})




def ordering(request):
    return render(request,'order.html')




def search_order(request):
    if request.method == "POST":
        resturant = request.POST['resturant']
        Restaurants = Restaurant.objects.filter(name__contains = resturant) 

        return render(request,'search_order.html', {'resturant':resturant,'Restaurants':Restaurants})
    else:
        return render(request,'search_order.html',{})




def product(request,Restaurant__name):
    Restaurant_obj = Restaurant.objects.get(name=Restaurant__name)
    food = Products.objects.filter(Restaurant_name=Restaurant_obj)

    return render(request,'product.html',
    {'food':food})




def carts(request):
    if request.user.is_authenticated:
        customer = request.user
        orders , created = order.objects.get_or_create(customer=customer,complete=False)
        items = orders.cart_set.all()
        cartItems = orders.get_cart_items
    else:
        items = []
        orders = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = orders['get_cart_items']
        customer = request.user

    context = {'items':items,'orders':orders,'cartItems':cartItems,'customer':customer}
    return render(request,'cart.html',context)





@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        userData = UserProfile.objects.get(user = customer)
        orders , created = order.objects.get_or_create(customer=customer,complete=False)
        items = orders.cart_set.all()
    else:
        items = []
        orders = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        customer = request.user

    context = {'items':items,'orders':orders,'customer':customer,'userData':userData}
    return render(request,'checkout.html',context)





def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Products.objects.get(id=productId)
    orders , created = order.objects.get_or_create(customer=customer,complete=False)
    item , created = cart.objects.get_or_create(order=orders,product=product)

    if action == 'add':
        item.quantity = (item.quantity + 1)
    elif action == 'remove':
        item.quantity = (item.quantity - 1)

    item.save()

    if item.quantity <= 0:
        item.delete()
    return JsonResponse('Item was added',safe=False)






@csrf_exempt
def processOrder(request):
    print('Data: ',request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user
        orders , created = order.objects.get_or_create(customer=customer,complete=False)
        total = float(data['form']['total'])
        orders.transaction_id = transaction_id

        if total == orders.get_cart_total:
            orders.complete = True
        orders.save()

        if orders.complete == True:
            shippingAddress.objects.create(
                customer = customer,
                order = orders,
                address = data['form']['address'],
                phone = data['form']['phone_number'],
                city = data['form']['city'],
            )
    else:
        print('user is not logged in ..')
    return JsonResponse('Payment Complete!',safe=False)






def api(request):
    Restaurant_objs = Restaurant.objects.all()
    
    zipcode = request.GET.get('zipcode')
    km = request.GET.get('km')
    user_lat = None
    user_long = None
    
    if zipcode:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(int(zipcode))
        user_lat = location.latitude
        user_long = location.longitude 
    
    
    payload = []
    for Restaurant_obj in Restaurant_objs:
        result = {}
        result['name'] = Restaurant_obj.name
        result['image'] = Restaurant_obj.image
        result['description'] = Restaurant_obj.description
        result['zipcode'] = Restaurant_obj.zipcode
        result['lat'] = Restaurant_obj.lat
        if zipcode:
            first = (float(user_lat) , float(user_long))
            second = (float(Restaurant_obj.lat) , float(Restaurant_obj.lon))
            result['distance'] = int( great_circle(first , second).miles)
        
        payload.append(result)
        
        if km:
            if result['distance'] > int(km):
                payload.pop()
    return JsonResponse(payload , safe=False)


def admin_dash(request):
    return render(request,'admin_dashboard.html')