from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from .models import Business,Hood
from django.shortcuts import get_object_or_404


# Create your views here.
def home(request):
    hoods = Hood.objects.all()
    context ={
        'hoods':hoods
    }
    return render(request,'index.html',context)

# register view
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        hood = request.POST['hood']

        if User.objects.filter(username=username).exists():
            messages.info(request,'Username already exists')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email already exists')
            return redirect('register')
        else:
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,hood=hood)
            user.save()
            return redirect('login')
    hoods = Hood.objects.all()
    return render(request,'register.html',{'hoods':hoods})

# login view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# detail view
def hood_detail(request,id):
    hood = get_object_or_404(Hood,id=id)
    context = {
        'hood': hood
    }
    return render(request,'hood_detail.html',context)
