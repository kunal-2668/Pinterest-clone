from django.shortcuts import render,redirect , get_object_or_404
from .models import Pins,Profile,Comments
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def Pinterest_home(request):
    data = Pins.objects.order_by("?")
    pro = Profile.objects.all()
    return render (request,'index.html',{'data':data,'pro':pro})

@login_required(login_url='login')
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

                if User.objects.filter(username=username).exists():
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def Profile_page(request):
    if request.user.is_authenticated:
        if Profile.objects.filter(name__exact=request.user).exists():
            Profile_photo = Profile.objects.get(name__exact=request.user)
            data = Pins.objects.filter(created_by__exact=request.user).order_by('-created_on')
            return render(request,'profile.html',{'Profile_photo':Profile_photo,'data':data})
        else:
            data = Pins.objects.filter(created_by__exact=request.user).order_by('-created_on')
            return render(request,'profile.html',{'data':data})
    else:
        return redirect('login')


@login_required(login_url='login')
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


def searchPin(request):
    if request.method=='POST':
        searchinp=request.POST['searchinp']
        if Pins.objects.filter(Title__contains=searchinp).exists():
            data = Pins.objects.filter(Title__contains=searchinp)
            return render (request,'index.html',{'data':data})
        else:
            messages.error(request,'No Search Result')
            return redirect('home')

def readMore(request,id):
    data = Pins.objects.get(id=id)
    commentbox = Comments.objects.filter(Post=data.id)
    number_of_likes = data.number_of_likes()


    liked=False
    if data.likes.filter(id=request.user.id).exists():
        liked=True

    if Profile.objects.filter(name = data.created_by).exists():
        pro = Profile.objects.get(name = data.created_by)
        return render (request,'readMore.html',{'data':data,'comment':commentbox,'number_of_likes':number_of_likes,'liked':liked,"pro":pro})
    else:
        return render (request,'readMore.html',{'data':data,'comment':commentbox,'number_of_likes':number_of_likes,'liked':liked,})


def CommentBox(request):
    if request.method == 'POST':
        Post = int(request.POST['postid'])
        Comment = request.POST['comment']
        comment_by = int(request.POST['profileid'])

        dataid = Pins.objects.get(id=Post)
        print(dataid)
        dataname = User.objects.get(id=comment_by)
        Comments.objects.create(Post=dataid,Comment=Comment,comment_by=dataname)
        return redirect('readMore',id=Post )
    else:
        messages.error(request,'Comment Failed')
        return redirect('readMore',id=Post)


@login_required(login_url='login')
def DeleteCommentById(request,id,postid):
    Comments.objects.get(id=id).delete()
    return redirect('readMore',id=postid)


@login_required(login_url='login')
def LikePin(request,id):
    pin = get_object_or_404(Pins,id=request.POST['pin_id'])
    liked=False
    if pin.likes.filter(id=request.user.id).exists():
        pin.likes.remove(request.user)
        liked=False
    else:
        pin.likes.add(request.user)
        liked=True
    return redirect('readMore',id=id)

@login_required(login_url='login')
def deletePin(req,id):
    Pins.objects.get(id=id).delete()
    return redirect('home')

@login_required(login_url='login')
def showotherprofile(request,id):
    user = request.user
    pro = Profile.objects.get(id=id)
    data = Pins.objects.filter(created_by = pro.name)
    print(pro.name,user)
    return render(request,"soprofile.html",{"pro":pro,"data":data})
