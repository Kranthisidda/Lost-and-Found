from datetime import timezone
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import logout,authenticate,login
from helloapp.models import User_Details,Item_Details
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
import random
from django.contrib import messages

@login_required(login_url='login_user')
def home(request):
    print(request.session['username'])
    return render(request,'helloapp/home.html')

def move_home(request):
    
    return render(request,'signup.html')
@csrf_exempt
def signup_user(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

    
        
        if User.objects.filter(username=uname):
            messages.warning(request, "Username already exist!")
            return redirect('signup_user')
    
        
        if User.objects.filter(email=email):
            messages.warning(request, "email already exist!")
            return redirect('signup_user')
        

        my_user = User.objects.create_user(username=uname,password=password,email=email)
        my_user.save()
        messages.success(request, "Registration successful!! Please Login!")
        return redirect('login_user')

    return render(request, 'signup.html')

def login_user(request):

    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['username'] = username
            request.session['email'] = user.email
            print(request.session['email'])
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, "Invalid Credentials!!")
            return redirect('login_user')

    return render(request, 'helloapp/login.html')



def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    digits = "0123456789"
    otp = ""
    for _ in range(length):
        otp += random.choice(digits)
    return otp



def send_otp_email(email,otp):
    """Send OTP to the us email address."""
    subject = 'Your OTP for password reset'
    message = otp
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    

    try:
        send_mail(subject, message, from_email, recipient_list)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
    return HttpResponse("OK")
    

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        if user:
            request.session['otp'] = generate_otp() # Function to generate OTP
            request.session['email'] = email
            send_otp_email(email,request.session['otp'])
          # Function to send OTP via email
            return HttpResponse("otp sent") 
        else:
            return HttpResponse("Enter vaild Email")
    else:
        return render(request,'helloapp/forgot_password.html')
@csrf_exempt
def otp_verification(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        if otp_entered == request.session['otp']:
            return HttpResponse("otp verfication successfull")
        else:
            # Handle incorrect OTP
            return HttpResponse("Unsuccessfull")

@csrf_exempt    
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            user = User.objects.get(email = request.session['email'])
            user.password = new_password
            user.save()
            return redirect('login_user')
        else:
            return HttpResponse("passwords not matched")
        
def form(request):
    return render(request,'helloapp/form.html',{'username':request.session['username'],'email':request.session['email']})
from datetime import datetime
def store_item(request):
    if request.method == 'POST':
    # Retrieve form data (using a dictionary for clarity)
        user_data = {
            'username':request.POST.get('username'),
            'email': request.POST.get('email'),
            'mobile_number': request.POST.get('mobile_number',''),
            'branch': request.POST.get('branch'),  
            'item_details': request.POST.get('item_details'),
            'select_type': request.POST.get('select_type'),
            'time':str(datetime.now())[:19]
        }

    # 
        new_user = Item_Details(**user_data)
        new_user.save()

        return render(request, 'helloapp/success.html')   
    else:
        return render(request, 'helloapp/form.html') 


def view_all_items(request):
    items = Item_Details.objects.all()  # Get all item objects
    print(type(datetime.now()))
    return render(request, 'helloapp/list.html',  {'items': items,'username':request.session['username']})
def view_user_items(request):
    
    items = Item_Details.objects.filter(username=request.session['username'])
    if len(items) != 0:
        msg = ""
    else:
        msg = 'norecords'
    return render(request, 'helloapp/delete.html',  {'items': items,'msg':msg})


def delete_items(request):
    if request.method == 'POST':
        item_id = request.POST.get("item_id")
    
        item = Item_Details.objects.get(id = item_id)
        item.delete()
        return redirect('view_user_items')
    
def edit_items(request):
    if request.method == 'POST':
        item_id = request.POST.get('itemid')
        item = Item_Details.objects.get(id=item_id)
        print(item.item_details)
        first = item.select_type
        if first == 'LOST':
            second = 'FOUND'
        else:
            first = 'FOUND'
            second = 'LOST'
        print(item.select_type)
        return render(request,'helloapp/edit_items.html',{'item':item,'first':first,'second':second})

def store_edited_item(request):
    if request.method == 'POST':
    # Retrieve form data (using a dictionary for clarity)
        item_id = request.POST.get('item_id')    
        item = Item_Details.objects.get(id=item_id)

        item.username = request.POST.get('username')
        item.email = request.POST.get('email')
        item.mobile_number =  request.POST.get('mobile_number','')
        item.branch = request.POST.get('branch')  # Set a default empty string for optional branch
        item.item_details =  request.POST.get('item_details')
        item.select_type =  request.POST.get('select_type')
        item.item_id = request.POST.get('item_id')

        item.save()
        return redirect('view_user_items')
def logout_user(request):
    logout(request)
    return redirect('login_user')

def filter(request):
    category = request.POST.get('filter')
    items = Item_Details.objects.filter(select_type=category)
    for item in items:
        print(item.username)
    return HttpResponse(items.count())




