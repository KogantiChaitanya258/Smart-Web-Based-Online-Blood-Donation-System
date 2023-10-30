from django.contrib import admin
from django.urls import path
from myapp import views
from django.contrib.auth import views as v
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static





urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.Login,name='login'),
    path('contactus/',views.Contactus,name="contactus"),
    path('faq/',views.Faq,name="faq"),
    path('registration/',views.Registration,name='register'),
    path('home/',views.Home,name='home'),
    path('donorreg/',views.Donorreg,name="donorreg"),
    path('base/',views.Base,name="base"),
    path('searchdonor/',views.Searchdonor,name="searchdonor"),
    path('donorinf/',views.Donorinf,name="donorinf"),
    path('logout/',v.LogoutView.as_view(template_name='myapp/Login.html'),name='logout'),
    path('updatedonor/',views.Updatedonor,name="updatedonor"),
    path('profile/',views.Profile,name="profile"),
    path('',views.Logout,name='ulogout'),
    path('addrequest/<str:donorname>/<str:donortype>/',views.Addrequest,name='addrequest'),
    path('requests/',views.Requests,name='requests'),
    path('myrequests/',views.Myrequests,name='myrequests'),
    path('donorprofile/<str:donorname>/',views.Donorprofile,name='donorprofile'),
    path('barchart/',views.Barchart,name='barchart'),
    path('<str:dname>/<str:rname>/<str:rservice>/<str:mode>',views.Deletereq,name='deletereq'),
    path('<str:dname>/<str:rname>/<str:rservice>',views.Acceptreq,name='acceptreq'),
    path('bloodcamp/',views.Bloodcamp,name='bloodcamp'),
]
