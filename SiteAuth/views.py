import smtplib
import ssl
from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
# from .models import Profile
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

## to activate the user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse 
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.encoding import force_str ### it does not have force_text in 4.0 version of django
## for emails 
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.core.mail import BadHeaderError, send_mail
from django.core import mail 
from django.conf import settings

from django.core.mail.backends.smtp import EmailBackend
#### getting taken from utils.py
from .utils import TokenGenerator , generate_token


## reset password generator 
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import threading 

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()

# Signup/login
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if(password==password2):
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return render(request, 'auth/signup.html')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return render(request, 'auth/signup.html')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False
                user.save()
                
                ## get current site 
                current_site = get_current_site(request)
                email_subject = "Activate you Account"
                email_content = render_to_string('auth/activate.html', {
                    'user': user,
                    'domain':"127.0.0.1:8000",
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                })
                
                # send_mail(
                #     email_subject,
                #     email_content,
                #     settings.EMAIL_HOST_USER,
                #     [email],
                #     fail_silently=False,
                # )
                msg=EmailMultiAlternatives(
                    email_subject,
                    email_content,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                msg.content_subtype = "html"
                msg.send()
                # email_message = EmailMessage(subject, host me, user, )
                # email_message = EmailMessage(email_subject, email_content,settings.EMAIL_HOST_USER, [email],)
                # EmailThread(email_message).start()
                messages.info(request, 'Activate your account by clicking on the link sent to your email')
                return redirect('/SiteAuth/login/')
        else:
            messages.info(request, 'Password Not Matching')
            return render(request, 'auth/signup.html')
    else:
        
        return render(request, 'auth/signup.html')
 
class activateView(View):
    def get(self,request, uidb64, token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True 
            user.save()
            messages.info(request, "Account Activated Successfully")
            return redirect('/SiteAuth/login/')
        return render(request, 'auth/activatefail.html', status=401)

   
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password) 
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/Sitelogin/login')
    else:
        username = "bl"
        password = 123
        return render(request, 'auth/login.html', {'username':username, 'password':password})
    
@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)
    return redirect('login') 


class RequestRestEmail(View):
    def get(self, request):
        return render(request, 'auth/request-rest-email.html')
    def post(self, request):
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            ## get current site 
            current_site = get_current_site(request)
            email_subject = "Reset your password"
            email_content = render_to_string('auth/reset-user-password.html', {
                'user': user,
                'domain':"127.0.0.1:8000",
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user),
                
            })
            msg=EmailMultiAlternatives(email_subject, email_content, settings.EMAIL_HOST_USER, [email], )
            msg.content_subtype = "html"
            msg.send()
            messages.info(request, 'Password reset link sent to your email', email)
            return render(request, 'auth/request-rest-email.html') 
        
class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, "Password link is invalid")
                return render(request, 'auth/request-rest-email.html')
        except DjangoUnicodeDecodeError as identifier:
            pass 
        return render(request, 'auth/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context={
            'uidb64':uidb64,
            'token':token,
        }
        
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if(password!=password2):
            messages.info(request, 'Password Not Matching')
            return render(request, 'auth/set-new-password.html')
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully, Please Login With New Password")
            return redirect('/SiteAuth/login/')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "Something went wrong")
            return render(request, 'auth/set-new-password.html', context)