from multiprocessing import context
from unicodedata import name
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from .models import Business,Hood,Profile,Post
from django.shortcuts import get_object_or_404


# Create your views here.
def home(request):
    if request.method == 'POST':
        title = request.POST['title']
        post = request.POST['post']

        posts = Post(title=title,post=post)
        posts.save()
    hoods = Hood.objects.all()
    context ={
        'hoods':hoods,
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

# profile view
def profile_page(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('image')
        location = request.POST['location']
        name = request.POST['name']
        
        profile = Profile(profile_picture=profile_picture,name=name,location=location,user=request.user)
        profile.save()
        print(profile)
        return render(request,'profile.html',{'profile':profile})
    return render(request,'profile.html')

# detail view
def hood_detail(request,id):
    hood = get_object_or_404(Hood,id=id)
    business = Business.objects.filter(hood=hood)
    posts = Post.objects.filter(hood_id=id)
    return render(request,'hood_detail.html',{'business':business,'hood':hood,'posts':posts})


def submit_post(request,hood_id):
    users = request.user
    if request.method == 'POST':
        title = request.POST['title']
        post = request.POST['post']

        posts = Post.objects.filter(hood_id=hood_id).exists()
        if posts:
            posts = Post.objects.get(hood_id=hood_id)
            posts.title = title
            posts.post = post
            posts.save()
        else:
            hoods = Hood.objects.get(id=hood_id)
            posts = Post(hood=hoods,title=title,post=post)
            posts.save()
    return redirect('/')
