from tkinter import TRUE
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, timedelta
from .forms import *
from .models import *

# Create your views here.
def home(request):
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]
    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]

    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]
  
    context = {
        'occupation_all': occupation_all, 
        'language_all': language_all, 
        'religion_all': religion_all,
        'caste_all': caste_all,
       
        'city_all': city_all, 
        'state_all': state_all, 
        'country_all': country_all, 

    }
    return render(request, 'app/index.html', context)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def logout_view(request):
    logout(request)
    return redirect('home')

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


@csrf_exempt
def profile(request):
    profile = Profile.objects.get_or_create(user=request.user)
    print('ln 56 request.user.id ', request.user.id)
    if request.method == 'POST':
        print('ln 58 in views.profile')
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, 
                                   instance=request.user.profile,
                                   # instance=profile,
                                   )
        if u_form.is_valid() and p_form.is_valid():           
            u_form.save()
            p_form.save()
            
            messages.success(request, f'Your account has been updated!')
            return render(request, 'app/index.html')
            #return redirect('home') 

    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        # p_form = ProfileForm(instance=profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'app/profile.html', context)

@csrf_exempt
def seeprofile(request):
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]
    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]

    if request.method == "POST":        
        profile_id = request.POST.get('profile_id')             
        print('ln 1015 profile_id', profile_id)
        user = request.user # ok 
        print('ln 1017 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 1019 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 1022 gender, id ', user_profile_gender, profile_id)
            profile = Profile.objects.filter(gender='female', id=profile_id).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 'image',
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 532 profile_female ', profile)
            profile_id = profile_id
            print('ln 1032 profile_id ', profile_id)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', id=profile_id).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 1042 profile_male ', profile) 
            profile_id = profile_id
            print('ln 1044 profile_id ', profile_id)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_id': profile_id,
            'profilefor': profilefor,
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/seeprofile.html', context)
    
    context = {      
        'occupation_all': occupation_all, 
        'language_all': language_all, 
        'religion_all': religion_all,
        'caste_all': caste_all,        
        'city_all': city_all, 
        'state_all': state_all, 
        'country_all': country_all, 
    }
    return render(request, 'app/seeprofile.html', context)


@csrf_exempt
def new(request): 
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]
    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]
    
    
    if request.method == "POST":   
        language = request.POST.get('language')             
        print('ln 93 language ', language)
        language_all = [c[0] for c in Profile.language.field.choices] 
        context = {         
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }   
        return render(request, 'app/new.html', context)        
    else:        
        print('ln 209 request.method not post')


@csrf_exempt
def o_list(request):
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]
    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]

    print('ln 126 occupation_all ', occupation_all)
    if request.method == "POST":        
        occupation = request.POST.get('occupation')             
        print('ln 129 occupation ', occupation)

        user = request.user # ok 
        print('ln 132 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 134 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 137 gender, lang ', user_profile_gender, occupation)
            profile = Profile.objects.filter(gender='female', occupation=occupation).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 145 profile_female ', profile)
            profile_occupation = occupation
            print('ln 147 occupation ', profile_occupation)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', occupation=occupation).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 157 profile_male ', profile) 
            profile_occupation = occupation
            print('ln 159 occupation ', profile_occupation)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_occupation': profile_occupation,
            'profilefor': profilefor,          
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/o_list.html', context)
    else:        
        occupation = request.GET.get('occupation')             
        print('ln 180 occupation ', occupation)

        user = request.user # ok 
        print('ln 183 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 185 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 188 gender, occupation ', user_profile_gender, occupation)
            profile = Profile.objects.filter(gender='female', occupation=occupation).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 196 profile_female ', profile)
            profile_occupation = occupation
            print('ln 198 occupation ', profile_occupation)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', occupation=occupation).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 208 profile_male ', profile) 
            profile_occupation = occupation
            print('ln 210 occupation ', profile_occupation)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_occupation': profile_occupation,
            'profilefor': profilefor,          
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/o_list.html', context)



@csrf_exempt
def city_list(request):
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]
    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]

    if request.method == "POST":        
        city = request.POST.get('city')             
        print('ln 188 city ', city)

        user = request.user # ok 
        print('ln 191 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 193 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 196 gender, city ', user_profile_gender, city)
            profile = Profile.objects.filter(gender='female', city=city).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 204 profile_female ', profile)
            profile_city = city
            print('ln 206 city ', profile_city)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', city=city).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 216 profile_male ', profile) 
            profile_city = city
            print('ln 218 city ', profile_city)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_city': profile_city,
            'profilefor': profilefor,  
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/city_list.html', context)
    else:        
        city = request.GET.get('city')             
        print('ln 244 city ', city)

        user = request.user # ok 
        print('ln 191 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 193 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 196 gender, city ', user_profile_gender, city)
            profile = Profile.objects.filter(gender='female', city=city).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 204 profile_female ', profile)
            profile_city = city
            print('ln 206 city ', profile_city)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', city=city).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 216 profile_male ', profile) 
            profile_city = city
            print('ln 218 city ', profile_city)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_city': profile_city,
            'profilefor': profilefor,  
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/city_list.html', context)


@csrf_exempt
def c_list(request):
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]
    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]

    if request.method == "POST":        
        caste = request.POST.get('caste')             
        print('ln 251 caste ', caste)

        user = request.user # ok 
        print('ln 254 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 256 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 174 gender, lang ', user_profile_gender, caste)
            profile = Profile.objects.filter(gender='female', caste=caste).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 267 profile_female ', profile)
            profile_caste = caste
            print('ln 269 caste ', profile_caste)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', caste=caste).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 279 profile_male ', profile) 
            profile_caste = caste
            print('ln 281 language ', profile_caste)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_caste': profile_caste,
            'profilefor': profilefor,          
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/c_list.html', context)
    else:        
        caste = request.GET.get('caste')             
        print('ln 251 caste ', caste)

        user = request.user # ok 
        print('ln 254 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 256 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 174 gender, lang ', user_profile_gender, caste)
            profile = Profile.objects.filter(gender='female', caste=caste).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 267 profile_female ', profile)
            profile_caste = caste
            print('ln 269 caste ', profile_caste)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', caste=caste).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 279 profile_male ', profile) 
            profile_caste = caste
            print('ln 281 language ', profile_caste)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_caste': profile_caste,
            'profilefor': profilefor,          
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/c_list.html', context)


@csrf_exempt
def r_list(request):
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]
    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]

    if request.method == "POST":        
        religion = request.POST.get('religion')             
        print('ln 314 religion ', religion)

        user = request.user # ok 
        print('ln 317 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 319 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 322 gender, lang ', user_profile_gender, religion)
            profile = Profile.objects.filter(gender='female', religion=religion).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 330 profile_female ', profile)
            profile_religion = religion
            print('ln 332 religion ', profile_religion)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', religion=religion).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 342 profile_male ', profile) 
            profile_religion = religion
            print('ln 344 language ', profile_religion)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_religion': profile_religion,
            'profilefor': profilefor,         
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/r_list.html', context)
    else:        
        religion = request.GET.get('religion')             
        print('ln 418 religion ', religion)

        user = request.user # ok 
        print('ln 421 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 423 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 426 gender, lang ', user_profile_gender, religion)
            profile = Profile.objects.filter(gender='female', religion=religion).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 434 profile_female ', profile)
            profile_religion = religion
            print('ln 436 religion ', profile_religion)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', religion=religion).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 446 profile_male ', profile) 
            profile_religion = religion
            print('ln 448 language ', profile_religion)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_religion': profile_religion,
            'profilefor': profilefor,         
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/r_list.html', context)



@csrf_exempt
def s_list(request):
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]
    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]

    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]
   
    
    if request.method == "POST":        
        state = request.POST.get('state')             
        print('ln 380 state ', state)

        user = request.user # ok 
        print('ln 383 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 385 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 388 gender, state ', user_profile_gender, state)
            profile = Profile.objects.filter(gender='female', state=state).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 396 profile_female ', profile)
            profile_state = state
            print('ln 398 state ', profile_state)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', state=state).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 408 profile_male ', profile) 
            profile_state = state
            print('ln 410 state ', profile_state)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_state': profile_state,
            'profilefor': profilefor,
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/s_list.html', context)
    else:        
        state = request.GET.get('state')             
        print('ln 380 state ', state)

        user = request.user # ok 
        print('ln 383 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 385 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 388 gender, state ', user_profile_gender, state)
            profile = Profile.objects.filter(gender='female', state=state).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 396 profile_female ', profile)
            profile_state = state
            print('ln 398 state ', profile_state)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', state=state).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 408 profile_male ', profile) 
            profile_state = state
            print('ln 410 state ', profile_state)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_state': profile_state,
            'profilefor': profilefor,
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/s_list.html', context)
         


@csrf_exempt
def nri_list(request):
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]
    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]
      
    if request.method == "POST":        
        country = request.POST.get('country')             
        print('ln 443 country ', country)

        user = request.user # ok 
        print('ln 446 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 448 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 451 gender, country ', user_profile_gender, country)
            profile = Profile.objects.filter(gender='female', country=country).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 459 profile_female ', profile)
            profile_country = country
            print('ln 461 country ', profile_country)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', country=country).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 471 profile_male ', profile) 
            profile_country = country
            print('ln 473 country ', profile_country)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_country': profile_country,
            'profilefor': profilefor,
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/nri_list.html', context)
    else:        
        country = request.GET.get('country')             
        print('ln 443 country ', country)

        user = request.user # ok 
        print('ln 446 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 448 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 451 gender, country ', user_profile_gender, country)
            profile = Profile.objects.filter(gender='female', country=country).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 459 profile_female ', profile)
            profile_country = country
            print('ln 461 country ', profile_country)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', country=country).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 471 profile_male ', profile) 
            profile_country = country
            print('ln 473 country ', profile_country)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_country': profile_country,
            'profilefor': profilefor,
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
#         return render(request, 'app/nri_list.html', context)

# def image_upload(request):
#     print('ln 865 from image_upload top')
#     if request.method == 'POST':
#         print('ln 866 from image_upload.POST')
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             # Get the current instance object to display in the template
#             img_obj = form.instance
#             print('ln 871 img_obj ', img_obj)
#             return render(request, 'app/image_upload.html', {'form': form, 'img_obj': img_obj})
#     else:
#         print('ln 875 from image_upload.GET')
#         form = ImageForm() 
#         return render(request, 'app/image_upload.html', {'form': form})

# def image_view(request):
#     if request.method == 'POST':
#         print('ln 879 from image_view.POST ')
#         form = ImageForm(request.POST, request.FILES) 
#         print('ln 884 form ', form)       
#         if form.is_valid():
#             form.save()
#             # Get the current instance object to display in the template
#             img_obj = form.instance
#             print('ln 889 img_obj ', img_obj)
#             print('ln 890 img_obj.title', img_obj.title)
#             print('ln 891 img_obj.image.url', img_obj.image.url)
#             return render(request, 'app/image_view.html', {'form': form, 'img_obj': img_obj})
    # else:
    #     print('ln 887 from image_view.get')
    #     form = ImageForm() 
    #     return render(request, 'app/image_view.html', {'form': form})


@csrf_exempt
def showallusers(request):
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]
    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]

    if request.method == 'POST':
        print('ln 922 in showallusers POST')
    else:
        #language = request.GET.get('language')   
        language = 'language1'           
        print('ln 943 language ', language)
        user = request.user # ok 
        print('ln 945 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 947 user_profile_gender ', user_profile_gender)  # ok
        
        if user_profile_gender == ['male']:
            print('ln 950 gender, lang ', user_profile_gender, language)
           # profile = Profile.objects.filter(gender='female', language=language)
            data = Profile.objects.filter(gender='female', language=language)
            print('ln 936 data ', data.values())             
            
          
            profile_language = language
            print('ln 958 language ', profile_language)  

            profilefor = 'BRIDES_LIST'     

        now_year = datetime.now().date().year 

        context = {           
            'data': data,
            'now_year': now_year,
            'profile_language': profile_language,
            'profilefor': profilefor,
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, "app/showallusers.html", context)
                


@csrf_exempt
def l_list(request): 
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]
    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]
 
    if request.method == "POST":        
        language = request.POST.get('language')             
        print('ln 888 language ', language)

        user = request.user # ok 
        print('ln 891 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 893 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 896 gender, lang ', user_profile_gender, language)
            profile = Profile.objects.filter(gender='female', language=language).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 'image',
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )

            print('ln 907 profile_female ', profile)
            # print('ln 908 profile.image ', profile.image  )
            profile_language = language
            print('ln 910 language ', profile_language)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', language=language).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 'image',
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 920 profile_male ', profile) 
            profile_language = language
            print('ln 922 language ', profile_language)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_language': profile_language,
            'profilefor': profilefor,
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/l_list.html', context)
    else: 
        language = request.GET.get('language')             
        print('ln 943 language ', language)
        user = request.user # ok 
        print('ln 945 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 947 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 950 gender, lang ', user_profile_gender, language)
            data = Profile.objects.filter(gender='female', language=language)            
            print('ln 936 data ', data.values())             
                
            # print('ln 956 profile_female ', profile)
            profile_language = language
            print('ln 958 language ', profile_language)  

            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', language=language).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 'image',
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 970 profile_male ', profile) 
            profile_language = language
            print('ln 972 language ', profile_language)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'data': data,
            'now_year': now_year,
            'profile_language': profile_language,
            'profilefor': profilefor,
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/l_list.html', context)


def about(request):
    lang_all = [c[0] for c in Profile.language.field.choices]
    context = {
        'lang_all': lang_all
    }
    return render(request, 'app/about.html', context)

def contact(request):
    lang_all = [c[0] for c in Profile.language.field.choices]
    context = {
        'lang_all': lang_all
    }
    return render(request, 'app/contact.html', context)

@csrf_exempt
def app(request):
    lang_all = [c[0] for c in Profile.language.field.choices]
    context = {
        'lang_all': lang_all
    }
    return render(request, 'app/app.html', context)

def assisted_services(request):
    return render(request, 'app/assisted_services.html')

def faq(request):
    return render(request, 'app/faq.html')

def matches(request):
    return render(request, 'app/matches.html')

@csrf_exempt
def search(request):
    occupation_all = [c[0] for c in Profile.occupation.field.choices]
    language_all = [c[0] for c in Profile.language.field.choices]    
    religion_all = [c[0] for c in Profile.religion.field.choices]
    caste_all = [c[0] for c in Profile.caste.field.choices]
    city_all = [c[0] for c in Profile.city.field.choices]
    state_all = [c[0] for c in Profile.state.field.choices]
    country_all = [c[0] for c in Profile.country.field.choices]
 
    if request.method == "POST":        
        profile_id = request.POST.get('profile_id')             
        print('ln 964 profile_id', profile_id)
        user = request.user # ok 
        print('ln 966 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 968 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 971 gender, id ', user_profile_gender, profile_id)
            profile = Profile.objects.filter(gender='female', id=profile_id).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            # print('ln 532 profile_female ', profile)
            profile_id = profile_id
            print('ln 981 profile_id ', profile_id)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', id=profile_id).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 991 profile_male ', profile) 
            profile_id = profile_id
            print('ln 993 profile_id ', profile_id)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_id': profile_id,
            'profilefor': profilefor,
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/search.html', context)

    elif request.method == "GET":        
        profile_id = request.GET.get('profile_id')             
        print('ln 1015 profile_id', profile_id)
        user = request.user # ok 
        print('ln 1017 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 1019 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 1022 gender, id ', user_profile_gender, profile_id)
            profile = Profile.objects.filter(gender='female', id=profile_id).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )        
            print('ln 532 profile_female ', profile)
            profile_id = profile_id
            print('ln 1032 profile_id ', profile_id)   
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            profile =  Profile.objects.filter(gender='male', id=profile_id).values(
            'user', 'user__username', 'user__email',
            'gender', 'birth_date', 'height', 'bio', 
            'qualification', 'occupation', 'salary',
            'language', 'caste', 'religion', 
            'city', 'state', 'country' 
            )
            print('ln 1042 profile_male ', profile) 
            profile_id = profile_id
            print('ln 1044 profile_id ', profile_id)   
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'profile': profile, 
            'now_year': now_year,
            'profile_id': profile_id,
            'profilefor': profilefor,
            'occupation_all': occupation_all, 
            'language_all': language_all, 
            'religion_all': religion_all,
            'caste_all': caste_all,        
            'city_all': city_all, 
            'state_all': state_all, 
            'country_all': country_all, 
        }
        return render(request, 'app/search.html', context)
    
    else:
        return render(request, 'app/search.html', context)
    


@csrf_exempt
def quick_search(request):
    lang_all = [c[0] for c in Profile.language.field.choices]
    context = {
        'lang_all': lang_all
    }
    return render(request, 'app/quick_search.html', context)


def terms(request):
    return render(request, 'app/terms.html')



