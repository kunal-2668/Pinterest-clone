from django.shortcuts import render,redirect
from .models import Pins,Profile
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.

def Pinterest_home(request):
    data = Pins.objects.order_by("?")
    return render (request,'index.html',{'data':data})


def add_pin(request):
    if request.method == 'POST':
        Pin = request.FILES['Pin']
        Title = request.POST['Title']
        Description = request.POST['Description']
        created_by = request.user
        Pins.objects.create(Pin=Pin,Title=Title,Description=Description,created_by=created_by)

        return redirect('home')


def Signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if len(password) >= 8 and password == password2 :
    
                if User.objects.filter(username=email).exists():
                    messages.error(request,'Username Already Exists')
                    return redirect('login')

                elif User.objects.filter(email=email).exists():
                    messages.error(request,'Email Already Exists')
                    return redirect('login')

                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    messages.info(request,'Account Created')
                    return redirect('login')
            else:
                messages.error(request,'Password should contains atleast 8 Characters!! or Try Matching Password!')
                return redirect('login')

        return render (request,'login.html')
    

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
  
            user = auth.authenticate(username=username,password=password)

            if user is not None:
                auth.login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Invalid Username/ Password')
                return redirect('login')
        
        return render (request,'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def addprofile(request):
    if request.user.is_authenticated:
        if Profile.objects.filter(name__exact=request.user).exists():
            return redirect('profile')
        elif request.method == "POST":
            profile_photo = request.FILES['profile_photo']
            Profile.objects.create(name=request.user,profile_photo=profile_photo)
            return redirect('profile')
        else:
            return render(request,'add_Profile.html')
    else:
        return redirect('login')


def Profile_page(request):
    if request.user.is_authenticated:
        if Profile.objects.filter(name__exact=request.user).exists():
            Profile_photo = Profile.objects.get(name__exact=request.user)
            data = Pins.objects.filter(created_by__exact=request.user)
            return render(request,'profile.html',{'Profile_photo':Profile_photo,'data':data})
        else:
            data = Pins.objects.filter(created_by__exact=request.user)
            return render(request,'profile.html',{'data':data})
    else:
        return redirect('login')
    

def update_profile(request,id):  
    data = Profile.objects.get(id=id)
    if request.user.is_authenticated:
        if Profile.objects.filter(name__exact=request.user).exists():
            if request.method == "POST":
                profile_photo = request.FILES['profile_photo']
                Profile(id=id,name=data.name,profile_photo=profile_photo).save()
                return redirect('profile')
            else:
                return render(request,'add_Profile.html')
        else:
            return redirect('profile')
    else:
        return redirect('login')


'''
  
def Connect(request):
    if request.method == 'GET':
        form = ConnectForm()
        return render(request,'connect_page.html',{'form':form})
    else:
        form = ConnectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

'''
 