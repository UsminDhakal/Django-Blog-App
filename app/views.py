from django.shortcuts import render,redirect
from .forms import UserSignup ,UserLogin,PostForm
from django.contrib import messages
from .models import BlogPost
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    blogs=BlogPost.objects.all()
    return render(request,"app/home.html",{'blogs':blogs})

def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")

def dashboard(request):
    if request.user.is_authenticated:
        blogs=BlogPost.objects.all()
        user=request.user
        fullname=user.get_full_name()
        gps=user.groups.all()
        return render(request,"app/dashboard.html",{'blogs':blogs,"fullname":fullname,'groups':gps})
    else:
        return redirect('/login/')

def user_logout(request):
    logout(request)
    return redirect('/login/')

def user_signup(request):
    if request.method=="POST":
        form= UserSignup(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulation,Your account has been created successfully. Now you can add blogs!!")
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
            
    else:
        form=UserSignup()

    return render(request,"app/signup.html",{'forms':form})

def login_user(request):
    if request.user.is_authenticated:
      return redirect("/dashboard/")
    else:
        if request.method=="POST":

            form=UserLogin(request,request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user=authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request,"User logged in successfully")
                    return redirect('/dashboard/')
        else:
            form=UserLogin()
        return render(request,"app/login.html",{'forms':form})


def addblog(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=PostForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                blg=BlogPost(title=title,desc=desc)
                blg.save()
                form=PostForm()
        else:
            form=PostForm()
        return render(request,'app/addblog.html',{'forms':form})
    else:
        return render('/login/')
    

def updateblog(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=BlogPost.objects.get(pk=id)
            form=PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi=BlogPost.objects.get(pk=id)
            form=PostForm(instance=pi)

        return render(request,'app/updateblog.html',{'forms':form})
    else:
        return render('/login/')
    
def deleteblog(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=BlogPost.objects.get(pk=id)
            pi.delete()
            return redirect('/dashboard/')

    else:
        return render('/login/')