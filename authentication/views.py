from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate , login , logout
from RLS import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.
def home(request):
     return render(request, "authentication/index.html")

def register(request):

     if request.method == "POST":
          username = request.POST['username']
          firstname = request.POST['firstname']
          lastname = request.POST['lastname']
          email = request.POST['email']
          pass1 = request.POST['pass1']
          pass_word_confirm = request.POST['pass_word_confirm']


          if User.objects.filter(username=username):
              messages.error(request, "Username Already Exist")
              return redirect('home')
          
          if User.objects.filter(email=email):
              messages.error(request, "Email Already Registed")

          
          if len(username)>25:
              messages.error(request, "Username Must be under 25 Character")

          if pass1 != pass_word_confirm:
              messages.error(request, "Passwords didn't match!")

          if not username.isalnum():
              messages.error(request, "Username must be Alpha-Numeric!")
              return redirect('home') 

              
          
          user = User.objects.create_user(username, email, pass1)
          user.first_name = firstname
          user.last_name = lastname 
          user.is_active = False
          user.save()

          messages.success(request, "Yaaaay! Your account has been created successfully.")


          # Welcome Email
          subject = "Welcome to RLS System!"
          message = "Hello " + user.first_name + "!! \n" + "Welcome to RLS!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nMohannad Bassem"        
          from_email = settings.DEFAULT_FROM_EMAIL
          to_list = [user.email]
          send_mail(subject, message, from_email, to_list, fail_silently=False)
         


          # Confirmation Email
           





          return redirect('signin')

     return render(request, "authentication/register.html")



def signin(request):

 if request.method == "POST":
      username = request.POST['username']
      pass1 = request.POST['pass1']

      user = authenticate(username=username , password=pass1)
     
      if user is not None:
          login(request, user)
          firstname = user.first_name
          return render(request, "authentication/index.html", {'firstname': firstname})

      else:
          messages.error(request, "Wrong Username or Password")
          return redirect('home')

 return render(request, "authentication/signin.html")

def signout(request):
     logout(request)
     messages.success(request, "You are Logged Out!")

     return redirect('home')

