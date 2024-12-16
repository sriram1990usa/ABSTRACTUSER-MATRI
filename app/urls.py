from django.urls import path
from .views import *
from django.views.generic import CreateView 

urlpatterns = [
    path('', home, name='home'),
    path("signup/", csrf_exempt(SignUpView.as_view()), name='signup'),    
   # path('register/', register, name ='register'),
    path('logout/', logout_view, name='logout'),    
    path('new/', new, name='new'),
    
    path('profile', profile, name='profile'),  
    path('seeprofile/', seeprofile, name='seeprofile'),
    path('showallprofiles', showallprofiles, name='showallprofiles'), 

    path('showuserallpics', showuserallpics, name='showuserallpics'),
 
    path('image_upload/', image_upload, name="image_upload"),
    path('image_view', image_view, name="image_view"),
    path('otherpic/<int:id>', otherpic, name='otherpic'),
    path('about/', about, name='about'),     
    path('contact/', contact, name='contact'), 

    path('app/', app, name='app'),   
    path('assisted_services/', assisted_services , name='assisted_services'),    
    
    path('o_list/', o_list , name='o_list'),  

    path('r_list/', r_list , name='r_list'),  
    path('c_list/', c_list , name='c_list'),
    path('l_list/', l_list, name='l_list'),  
    # path('l_list/?language=language', l_list, name="l_list"),         
   
    path('city_list/', city_list, name='city_list'),
    path('s_list/', s_list , name='s_list'), 
    path('nri_list/', nri_list, name='nri_list'),  

    path('faq/', faq, name='faq'),       
    # path('form_entry/', form_entry, name='form_entry'), 
    path('matches/', matches, name='matches'),
    path('search/', search, name='search'),    
    
    path('quick_search', quick_search, name='quick_search'),  
    path('terms/', terms, name='terms'),    
]