from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import random, string
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q


def home(request):
    return render(request, 'homepage.html')
def about(request):
    return render(request, 'aboutus.html')
def contact(request):
    return render(request, 'contact.html')
def registration(request):
    return render(request, 'registration.html')
def newpass(request):
    return render(request, 'set_new_password.html')
def sign(request):
    return render(request, 'signup.html')



def display_form(request):
    if request.method=='POST':
        forms=studentform(request.POST, request.FILES)
        if forms.is_valid():
            myname=forms.cleaned_data['name']
            myage=forms.cleaned_data['age']
            myemail=forms.cleaned_data['email']
            mygender=forms.cleaned_data['gender']
            mydob=forms.cleaned_data['date_of_birth']
            myphno=forms.cleaned_data['phone_number']
            mycountry=forms.cleaned_data['country']
            mystate=forms.cleaned_data['state']
            mydistrict=forms.cleaned_data['district']
            mycity=forms.cleaned_data['city']
            myhobbies=forms.cleaned_data['hobbies']
            student.objects.create(name=myname, age=myage, email=myemail, gender=mygender, date_of_birth=mydob, phone_number=myphno,
                        country=mycountry, state=mystate, district=mydistrict, city=mycity, hobbies=myhobbies, file=forms.cleaned_data['file']).save()
            messages.success(request, 'Registration successful!')
            return render(request, 'message.html', {'forms': forms}) 
            return HttpResponse('success')
        else:
            return render(request, 'registration.html', {'forms':forms})
    else:
        forms=studentform()
        return render(request, 'registration.html', {'forms':forms})
    

def mail_send(request):
    if request.method =='POST':
        to_email='narmathanarmu186@gmail.com'
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_mail=request.POST.get('email')
        file= request.FILES.get('file')
        
        obj=EmailMessage(subject, message, from_mail,[to_email])
        if file:
            obj.attach(file.name, file.read(), file.content_type)
        obj.send()
        
        user_email = request.POST.get('email')
        auto_subject = 'Hello!'
        auto_message = 'Thank you for contacting us. We will contact you soon. Stay tuned!'
        
        auto_reply = EmailMessage(auto_subject, auto_message, to_email, [user_email])
        auto_reply.send()

        messages.success(request, 'Mail sent successfully and auto-reply sent.')
        return render(request, 'mailsend.html')
    else:
        return render(request, 'mail.html')


def gen_pass(request):
    if request.method == "GET":
        to_email = request.GET.get('email')

        if not to_email:
            return HttpResponse("Email is required!", status=400)

        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        TempUser.objects.update_or_create(
            email=to_email,
            defaults={'temp_password': temp_password}
        )
        
        from_mail = 'narmathanarmu186@gmail.com'
        subject = 'Your Temporary Password'
        message = f"""
        Hello,

        Your temporary password is: {temp_password}

        Please use this password to log in and create a new password.

        Regards,
        Your Website Team
        """
        
        try:
            email_obj = EmailMessage(subject, message, from_mail, [to_email])
            email_obj.send()
            return render(request, 'verify.html', {'message': 'Temporary password sent successfully!'})
        except Exception as e:
            return HttpResponse(f"Failed to send email: {e}", status=500)
    
    return HttpResponse("Only GET method is allowed", status=405)




def verify_temp_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        temp_pass = request.POST.get('password')

        try:
            user = TempUser.objects.get(email=email)
            if user.temp_password == temp_pass:
                request.session['verified_email'] = email
                return redirect('set_new_password')
            else:
                return render(request, 'verify.html', {'error': 'Invalid temporary password.'})
        except TempUser.DoesNotExist:
            return render(request, 'verify.html', {'error': 'Email not found.'})
    return render(request, 'verify.html')


def set_new_password(request):
    email = request.session.get('verified_email')
    if not email:
        return redirect('verify_temp_password')

    if request.method == "POST":
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')

        if new_pass == confirm_pass:
            user = TempUser.objects.get(email=email)
            user.new_password = make_password(new_pass)  # hashed password
            user.save()
            return redirect('login')
        else:
            return render(request, 'set_new_password.html', {'error': 'Passwords do not match.'})
    return render(request, 'set_new_password.html')

       
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import TempUser

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'login.html', {'error': 'Email and password are required.'})

        email = email.strip() 

        try:
            
            user = TempUser.objects.get(Q(email__iexact=email))

            if check_password(password, user.new_password): 
                request.session['user_email'] = user.email
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'error': 'Incorrect password.'})

        except TempUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email not registered.'})

    return render(request, 'login.html')





def dashboard(request):
    email = request.session.get('user_email')  # email saved during login

    if not email:
        return redirect('login')  # redirect if session expired or user not logged in

    try:
        user = student.objects.get(email=email)
        context = {
            'user': user
        }
        return render(request, 'dashboard.html', context)
    except student.DoesNotExist:
        return render(request, 'dashboard.html', {'error': 'No student data found for this email.'})

    
    
def logout_view(request):
    request.session.flush()  # clear all session data
    return redirect('login')
