from . import views
from django.urls import path,include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("ownerhome",views.ownerhome,name="ownerhome"),
    #path('report_builder/', include('report_builder.urls')),
    path("register",views.Register,name="register"),
    path('login', views.Login, name='login'),
    path('logout', views.Logout, name='logout'),
    path('collection', views.collectionhome, name='collection'),
    path('activate/<uidb64>/<token>', verification_View.as_view(),name='activate'),
    path("",views.home,name="home"),
    path('profile',ProfileView.as_view(),name='profile'),
    path('edit_profile',csrf_exempt(ProfileSet.as_view()),name='edit_profile'),
    path("ownerregister",views.ownerregister,name="ownerregister"),
    path("ownerlogin",views.ownerlogin,name="ownerlogin"),
    path("addnew",views.addnew,name="addnew"),
    
    ]