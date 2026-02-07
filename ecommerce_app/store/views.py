from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User

def home(request):
    isadminuser = False
    if request.user.is_authenticated:
        isadminuser = request.user.is_superuser
    context = {
        "isadminuser" : isadminuser
    }
    return render(request,'store/home.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            return render(request, 'store/register.html',{'error': 'email already exists'})
        else:
            User.objects.create_user(username=username,email=email, password=password)
            return redirect('store:login')
    return render(request, 'store/register.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect('store:home')
            else :
                return render(request,'store/login.html',{'error' : 'Invalid credentials'})
        except User.DoesNotExist:
            return render(request, 'store/login.html', {'error': 'User with this email does not exist'})
    return render(request, 'store/login.html')

def logout_user(request):
    logout(request)
    return redirect('store:login')