from django.shortcuts import render,redirect
from .forms import Createuserforms
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from .decorators import autheticatedfor_adminonly
from django.db.models import Q
from django.views.decorators.cache import never_cache






# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if 'username' in request.session:
        return render(request,'index.html')
    return redirect(login)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if 'username' in request.session:
        return redirect(index)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # login(request,user)
            auth.login(request,user)
            request.session['username'] = username
            messages.success(request, 'Welcome !!!')
            return redirect('/')
        else:
            messages.error(request, '*Invalid Username or Password')
            return redirect(login)
    return render(request,'login.html')



@autheticatedfor_adminonly
def register(request): 
    mydata = User.objects.all()
    if(mydata != ''):
        return render(request, 'userdata.html', {'datas': mydata})
    else:
        return render(request, 'register.html')  



def addData(request):
    if 'username'  in request.session:
        return redirect(index)
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1 == password2):
                if User.objects.filter(username=name).exists():
                    messages.info(request,"Username is already taken")
                    return redirect(addData)
                elif email=="":
                    messages.error(request,"EmailField  is empty")
                    return redirect(addData)
                elif User.objects.filter(email=email).exists():
                    messages.info(request,"Email is already taken")
                    return redirect(addData)
                else:

                    user = User.objects.create_user(
                    username=name, email=email, password=password1)  
                    user.save()
                    messages.success(request, 'Account has been Created Succesfully')
                    return redirect(login)
        else:
            messages.warning(request, 'Password Mismatch Found...!!')
            return redirect(addData)  # name in url

    else:
        form = Createuserforms()
        return render(request, 'register.html', {'form': form})


@autheticatedfor_adminonly
def addUser(request):
    

    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1 == password2):
            if User.objects.filter(username=name).exists():
                    messages.info(request,"Username is already taken")
                    return redirect(addUser)
            elif email=="":
                    messages.error(request,"EmailField  is empty")
                    return redirect(addUser)
            elif User.objects.filter(email=email).exists():
                    messages.info(request,"Email is already taken")
                    return redirect(addUser)
            else:
                user = User.objects.create_user(
                    username=name, email=email, password=password1) 
                user.save()
                messages.success(request, 'Account has been Created Succesfully')
                return redirect(userdata)
        else:
            messages.warning(request, 'Password Mismatch Found...!!')
            return redirect(addUser)  # name in url

    else:
        form = Createuserforms()
        return render(request, 'adduser.html', {'form': form})
     

@autheticatedfor_adminonly
def addAdmin(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1 == password2):
            if User.objects.filter(username=name).exists():
                    messages.info(request,"Username is already taken")
                    return redirect(addAdmin)
            elif email=="":
                     messages.error(request,"EmailField  is empty")
                     return redirect(addAdmin)
            elif User.objects.filter(email=email).exists():
                    messages.info(request,"Email is already taken")
            else:
                user = User.objects.create_user(
                    username=name, email=email, password=password1)  
                user.is_staff=True
                user.is_superuser=True
                user.save()
                messages.success(request, 'Account has been Created Succesfully')
                return redirect(userdata)
        else:
            messages.warning(request, 'Password Mismatch Found...!!')
            return redirect(addAdmin)  # name in url

    else:
        form = Createuserforms()
        return render(request, 'addAdmin.html', {'form': form})

@autheticatedfor_adminonly
def userdata(request):
    if 'q' in request.POST:
        q=request.POST['q']
        searchwith=Q(Q(username__icontains=q)|Q(email__icontains=q))
        mydata=User.objects.filter(searchwith)
    else:
        mydata = User.objects.all()
       
    return render(request, 'userdata.html', {'datas': mydata})


@autheticatedfor_adminonly
def update(request,id):
    mydata = User.objects.get(id=id)


    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        if name=="":
            messages.error(request,"username Field  is empty,Data is not Updated")
            redirect(userdata)
        elif email=="":
            messages.error(request,"Email Field  is empty,Data is not Updated")
            redirect(userdata)
        elif User.objects.exclude(id=id).filter(username=name).exists():
            messages.error(request,"Username is already taken,Try with Another Username....")
            redirect(userdata)
        elif User.objects.exclude(id=id).filter(email=email).exists():
            messages.error(request,"Email is already taken,Try with Another email......")
            redirect(userdata)
        else:
            mydata.username = name
            mydata.email = email
            mydata.save()
            messages.success(request,'Details are  Updated Successfully')
            return redirect(register)
    return render(request, 'update.html', {'data': mydata})

def deleteData(request,id):
    mydata = User.objects.get(id=id)
    mydata.delete()
    messages.error(request,'User is Deleted is Successfully')
    return redirect(userdata)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if 'username' in request.session:
       
        request.session.flush()
    # auth.logout(request)
    return render(request,'logout.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    obj = User.objects.all()
    return render(request,'home.html',{'user':obj})