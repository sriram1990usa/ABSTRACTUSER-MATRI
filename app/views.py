from tkinter import TRUE
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
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
    if request.method == 'POST':
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

    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'app/profile.html', context)

@csrf_exempt
def image_upload(request):
    print('ln 132 from image_upload top')
    if request.method == 'POST':
        user = request.user
        print('user.id ', user.id)
        
        profile = Profile.objects.get(user=request.user)
        form = AddimgUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'app/image_upload.html', {'form': form, 'img_obj': img_obj})
        else:
            print('ln 146 form.is_invalid')

        addimg = Addimg.objects.filter(profile_id=profile.id)
        print('ln 149 addimg ', addimg)
    
    else:
        form = AddimgUpdateForm() 
        return render(request, 'app/image_upload.html', {'form': form})
   
@csrf_exempt
def image_view(request):
    if request.method == 'POST':
        print('ln 159 from image_view.POST ')
    else:
        print('ln 161 from image_view.get')
        user = request.user # ok 
        print('ln 163 user, user.id ', user, user.id)
        profile = Profile.objects.filter(id=user.id)
        print('ln 165 profile ', profile.values())
        
        data = Addimg.objects.filter(profile_id=user.id)
        print('ln 169 photos ', data.values())     
        
        context = {           
            'data': data,
        }
        return render(request, "app/image_view.html", context)   

def otherpic(request, id):
    if request.method == 'POST':
        return render(request, 'app/about.html')
    else:
        user = CustomUser.objects.get(id=id)
        print('ln 173 user selected, user.id  ', user, user.id)
        profile = Profile.objects.filter(id=user.id)
        print('ln 151 profile ', profile.values())
        data = Addimg.objects.filter(profile_id=user.id)
        
        for image in Addimg.objects.filter(profile_id=user.id):
            print('ln 157 image of Addimg', image.propic)

        context = {           
            'data': data,
        }
        return render(request, "app/otherpic.html", context)  
   
@csrf_exempt
def showuserallpics(request):
    if request.method == 'POST':
        print('ln 119 in showallusers POST')
    else:
        user = request.user # ok 
        print('ln 122 user ', user)
        profile = Profile.objects.filter(id=user.id)
        print('ln 124 profile ', profile.values())
        print('ln 125 user_id ', user.id)
        data = Addimg.objects.filter(profile_id=user.id)
        print('ln 127 photos ', data.values())        
        
        for image in Addimg.objects.filter(profile_id=user.id):
            print('ln 131 image of Addimg', image.propic)

        context = {           
            'data': data,
        }
        return render(request, "app/showuserallpics.html", context)
        
@csrf_exempt
def showallprofiles(request):
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
        language = 'language1'        
        user = request.user # ok 
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        
        if user_profile_gender == ['male']:
            data = Profile.objects.filter(gender='female', language=language)
            profile_language = language
            profilefor = 'BRIDES_LIST'     
        elif user_profile_gender == ['female']:
            data = Profile.objects.filter(gender='male', language=language)

            print('ln 936 data ', data.values())
            profile_language = language
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
        return render(request, "app/showallprofiles.html", context)
    
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
        user = request.user # ok 
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))

        if user_profile_gender == ['male']:
            data = Profile.objects.filter(gender='female', id=profile_id)
            profile_id = profile_id
            profilefor = 'BRIDES_LIST'
        elif user_profile_gender == ['female']:        
            data =  Profile.objects.filter(gender='male', id=profile_id)
            profile_id = profile_id
            profilefor = 'GROOMS_LIST'  
          
        now_year = datetime.now().date().year 

        context = {           
            'data': data, 
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

    if request.method == "POST":        
        occupation = request.POST.get('occupation')    
    else:        
        occupation = request.GET.get('occupation') 
        user = request.user # ok 
        print('ln 183 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 185 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 188 gender, occupation ', user_profile_gender, occupation)
            data = Profile.objects.filter(gender='female', occupation=occupation)
            print('ln 936 data ', data.values())  
            profile_occupation = occupation 
            print('ln 958 occupation ', profile_occupation)
            profilefor = 'BRIDES_LIST'

        elif user_profile_gender == ['female']:        
            data =  Profile.objects.filter(gender='male', occupation=occupation)
            profile_occupation = occupation
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'data': data, 
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
    else:        
        city = request.GET.get('city')   
        user = request.user # ok 
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))

        if user_profile_gender == ['male']:
            data = Profile.objects.filter(gender='female', city=city)
            profile_city = city
            profilefor = 'BRIDES_LIST'

        elif user_profile_gender == ['female']:        
            data =  Profile.objects.filter(gender='male', city=city)
            profile_city = city
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'data': data, 
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
    else:        
        caste = request.GET.get('caste')             
        print('ln 251 caste ', caste)
        user = request.user # ok 
        print('ln 254 user ', user)
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 256 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            data = Profile.objects.filter(gender='female', caste=caste)
            profile_caste = caste
            profilefor = 'BRIDES_LIST'

        elif user_profile_gender == ['female']:        
            data =  Profile.objects.filter(gender='male', caste=caste)    
            profile_caste = caste
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'data': data, 
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
    else:        
        religion = request.GET.get('religion')    
        user = request.user # ok 
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
        print('ln 423 user_profile_gender ', user_profile_gender)  # ok

        if user_profile_gender == ['male']:
            print('ln 426 gender, lang ', user_profile_gender, religion)
            data = Profile.objects.filter(gender='female', religion=religion)
            print('ln 936 data ', data.values())      
            profile_religion = religion
            print('ln 436 religion ', profile_religion)   
            profilefor = 'BRIDES_LIST'

        elif user_profile_gender == ['female']:        
            data =  Profile.objects.filter(gender='male', religion=religion)
            profile_religion = religion
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'data': data, 
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
    else:        
        state = request.GET.get('state')    
        user = request.user # ok 
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))

        if user_profile_gender == ['male']:
            data = Profile.objects.filter(gender='female', state=state)
            profile_state = state
            profilefor = 'BRIDES_LIST'

        elif user_profile_gender == ['female']:        
            data =  Profile.objects.filter(gender='male', state=state)
            profile_state = state
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'data': data, 
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
    else:        
        country = request.GET.get('country')    
        user = request.user # ok 
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))

        if user_profile_gender == ['male']:
            data = Profile.objects.filter(gender='female', country=country)
            profile_country = country
            profilefor = 'BRIDES_LIST'

        elif user_profile_gender == ['female']:        
            data =  Profile.objects.filter(gender='male', country=country)
            profile_country = country
            profilefor = 'GROOMS_LIST'  

        now_year = datetime.now().date().year 

        context = {           
            'data': data, 
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
    else: 
        language = request.GET.get('language')     
        user = request.user # ok 
        user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))

        if user_profile_gender == ['male']:
            print('ln 950 gender, lang ', user_profile_gender, language)
            data = Profile.objects.filter(gender='female', language=language)
            profile_language = language
            profilefor = 'BRIDES_LIST'

        elif user_profile_gender == ['female']:
            data = Profile.objects.filter(gender='male', language=language)
            profile_language = language
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

    user = request.user
    if user.is_authenticated:
        if request.method == "POST":        
            profile_id = request.POST.get('profile_id')        
            user = request.user # ok 
            user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))

            if user_profile_gender == ['male']:
                profile = Profile.objects.filter(gender='female', id=profile_id).values(
                'user', 'user__username', 'user__email',
                'gender', 'birth_date', 'height', 'bio', 
                'qualification', 'occupation', 'salary',
                'language', 'caste', 'religion', 
                'city', 'state', 'country' 
                )        
                profile_id = profile_id
                profilefor = 'BRIDES_LIST'
            elif user_profile_gender == ['female']:        
                profile =  Profile.objects.filter(gender='male', id=profile_id).values(
                'user', 'user__username', 'user__email',
                'gender', 'birth_date', 'height', 'bio', 
                'qualification', 'occupation', 'salary',
                'language', 'caste', 'religion', 
                'city', 'state', 'country' 
                )
                profile_id = profile_id
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
            user = request.user # ok 
            user_profile_gender = list(Profile.objects.filter(user=user).values_list('gender', flat=True))
            if user_profile_gender == ['male']:
                print('ln 1022 gender, id ', user_profile_gender, profile_id)
                profile = Profile.objects.filter(gender='female', id=profile_id).values(
                'user', 'user__username', 'user__email',
                'gender', 'birth_date', 'height', 'bio', 
                'qualification', 'occupation', 'salary',
                'language', 'caste', 'religion', 
                'city', 'state', 'country' 
                )        
                profile_id = profile_id   
                profilefor = 'BRIDES_LIST'
            elif user_profile_gender == ['female']:        
                profile =  Profile.objects.filter(gender='male', id=profile_id).values(
                'user', 'user__username', 'user__email',
                'gender', 'birth_date', 'height', 'bio', 
                'qualification', 'occupation', 'salary',
                'language', 'caste', 'religion', 
                'city', 'state', 'country' 
                )
                profile_id = profile_id 
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
       
        return render(request, 'app/search.html')
    

@csrf_exempt
def quick_search(request):
    lang_all = [c[0] for c in Profile.language.field.choices]
    context = {
        'lang_all': lang_all
    }
    return render(request, 'app/quick_search.html', context)


def terms(request):
    return render(request, 'app/terms.html')
