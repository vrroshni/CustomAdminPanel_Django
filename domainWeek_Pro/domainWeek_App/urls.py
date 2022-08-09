from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='Index'),
    path('login',views.login,name='Login'),
    path('logout',views.logout,name='Logout'),
    path('register',views.register,name='Register'),
    path('home',views.home,name='Home'),
    path('addData',views.addData,name='AddData'),
    path('userData',views.userdata,name='userData'),
    path('addUser',views.addUser,name='AddUser'),
    path('addAdmin',views.addAdmin,name='AddAdmin'),
    path('update/<int:id>',views.update,name='Update'),
    path('delete/<int:id>',views.deleteData,name='Delete'),


    ]