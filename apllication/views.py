from collections.abc import Callable, Iterable, Mapping
from typing import Any
from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.urls import reverse
from django.views import View
from django.db.models import Q
import json
import threading
from django.http import JsonResponse
from django.conf import settings
from .forms import RegisterForm,UserLoginForm,ProfileForm,ArchiveForm,UserEditForm
# from .serializers import productSerializer
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import *
from django.core.mail import EmailMessage, BadHeaderError,send_mail
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from threading import Thread
from django.core.files.storage import FileSystemStorage


@login_required(login_url="ownerlogin")
def addnew(request):
    try:
        profile_obj = Profile.objects.get(owner=request.user, account="Author")
    except:
        return redirect("ownerlogin")
    if request.method=="POST":
        name=request.POST.get('name')
        description=request.POST.get('description')
        genre=request.POST.get('genre')
        file=request.FILES.get('file')
        image=request.FILES.get('image')
        try:
            owner=Archive_owner.objects.get(username=request.user.username)
        except:
           return redirect("ownerhome") 
        if file and image:
            # Save the file and image to the media directory
            fs = FileSystemStorage()
            file_name = fs.save(file.name, file)
            image_name = fs.save(image.name, image)
            
            # Create Archive object with file and image paths
            Archive.objects.create(
                name=name,
                owner=owner,
                description=description,
                type="PDF",
                genre=genre,
                file=file_name,  # Save the file path
                preview_image=image_name  # Save the image path
            )
            
            return render(request,"addnew.html",{"message":"File uploaded successfully!"})
        else:
            return render(request,"addnew.html",{"message":"File upload failed!"})
        
    return render(request,"addnew.html")
@login_required(login_url="ownerlogin")
def ownerhome(request):
    try:
        profile_obj = Profile.objects.get(owner=request.user, account="Author")
    except:
        return redirect("ownerlogin")
    archive_obj = Archive.objects.filter(owner__username=request.user.username)
    return render(request,'ownerhome.html',{'archives':archive_obj})
def ownerregister(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['email']
            username = form.cleaned_data['username']
            user = form.save()
            user.save()

            Archive_owner.objects.create(user=user, username=username)
            Profile.objects.create(owner=user, account='Author')
            # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            # domain = get_current_site(request).domain
            # link = reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
            # email_subject = 'Digitalibrary Account Activation'
            # activate_url = 'http://'+ domain + link
            # email_body = "Please click the link to activate your account" + activate_url
            # email_header = 'Digitalibrary Account Activation'
            # try:
            #     EmailThread(subject=email_subject, message=email_body, recipient_list=[mail]).start()
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found.')
            # except Exception as ex:
            #     print(f"Error sending email: {ex}")
            #     return HttpResponse('An error occurred while sending the email.')
            customer = Group.objects.get(name="SiteUSers")
            user.groups.add(customer)
            return redirect("ownerlogin")
        else:
            form.add_error(None, "Invalid email or password.")
            return render(request,'authentication/ownerregister.html',{'form':form})
       
    form = RegisterForm()
    return render(request,'authentication/ownerregister.html',{'form':form})
def ownerlogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = None  # Initialize user variable here
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error(None, "Invalid email or password.")
                return render(request, 'authentication/ownerlogin.html', {'form': form}) 
            print(user.username)
            if user is not None:
                if authenticate(request, username=user.username, password=password):
                    login(request, user)
                    if request.user.is_superuser:
                        return render(request,'root/admin.html')
                    else :
                        try:
                            profile_obj = Profile.objects.get(owner=request.user)
                            if profile_obj.account=="Author":
                                print("here")
                                return redirect('ownerhome')
                            else:
                                form.add_error(None, "Invalid email or password.")
                                return render(request, 'authentication/ownerlogin.html', {'form': form})
                        except:
                            form.add_error(None, "Invalid email or password.")
                            return render(request, 'authentication/ownerlogin.html', {'form': form})
                        
                else:
                    form.add_error(None, "Invalid email or password.") 
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        logout(request)
        form = UserLoginForm()
    return render(request, 'authentication/ownerlogin.html', {'form': form})
class EmailThread(Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        super(EmailThread, self).__init__()

    def run(self):
        send_mail(self.subject, self.message, settings.DEFAULT_FROM_EMAIL, self.recipient_list)

        
def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['email']
            user = form.save()
            user.save()

            Profile.objects.create(owner=user, account='Normal User')
            # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            # domain = get_current_site(request).domain
            # link = reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
            # email_subject = 'Digitalibrary Account Activation'
            # activate_url = 'http://'+ domain + link
            # email_body = "Please click the link to activate your account" + activate_url
            # email_header = 'Digitalibrary Account Activation'
            # try:
            #     EmailThread(subject=email_subject, message=email_body, recipient_list=[mail]).start()
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found.')
            # except Exception as ex:
            #     print(f"Error sending email: {ex}")
            #     return HttpResponse('An error occurred while sending the email.')
            customer = Group.objects.get(name="SiteUSers")
            user.groups.add(customer)
            return redirect("login")
        else:
            form.add_error(None, "Invalid email or password.")
            return redirect("login")
       
    form = RegisterForm()
    return render(request,'authentication/registration.html',{'form':form})

def home(request):
    return render(request,'root/home.html')


def Login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if email=="" or password=="":
                print("here")
            user = None  # Initialize user variable here
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                print("User does not exist")
            if user is not None:
                print(user)
                if authenticate(request, username=user.username, password=password):
                    login(request, user)
                    if request.user.is_superuser:
                        
                        return render(request,'root/admin.html')
                    else :
                        try:
                            profile_obj = Profile.objects.get(owner=request.user)
                            return redirect('collection')
                        except:
                            return render(request, 'authentication/login.html', {'form': form})
                        
                else:
                    form.add_error(None, "Invalid email or password.") 
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        logout(request)
        form = UserLoginForm()
    return render(request, 'authentication/login.html', {'form': form})
def Logout(request):
    logout(request)
    return redirect('home')

class verification_View(View):
    def get(self,request,uidb64,token):
        try:
            id =  force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user,token):
                return redirect('login'+'?message='+'User already activated')
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            return redirect('login')
        except Exception as ex:
            pass

        return redirect('login')
@login_required(login_url="login")
def collectionhome(request):
        try:
            profile_obj = Profile.objects.get(owner=request.user)
        except:
            return redirect("login")
        archive_obj = Archive.objects.all()
        return render(request,'root/archives.html',{'archives':archive_obj})
    
class ProfileSet( View):
    def get(self, request):
        form1 = ProfileForm()
        form2 = UserEditForm()
        return render(request, 'root/profile.html', {'form1': form1, 'form2': form2})
    def post(self, request):
        user_instance = request.user
        form1 = ProfileForm(request.POST, prefix='form1',instance=user_instance)
        form2 = UserEditForm(request.POST, prefix='form2',instance=user_instance)


        if 'form1-submit' in request.POST:
            if form1.is_valid():
                try:
                    profile = Profile.objects.get(owner=request.user)
                    print('profile found')
                    form1.save()
                    email_subject = 'Digitalibrary PROFILE UPDATE'
                    email_body = "Profile information updated successfully." 
                    email_header = 'Digitalibrary PROFILE UPDATE'
                    mail = request.user.email
                    try:
                        EmailThread(subject=email_subject, message=email_body, recipient_list=[mail]).start()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    except Exception as ex:
                        print(f"Error sending email: {ex}")
                        return HttpResponse('An error occurred while sending the email.')
                except Profile.DoesNotExist:
                    print("no profile found")
                return redirect('home')

        elif 'form2-submit' in request.POST:
            if form2.is_valid():
                form2.save()
                email_subject = 'Digitalibrary USER INFORMATION  UPDATE'
                email_body = "Your User information updated successfully." 
                email_header = 'Digitalibrary USER INFORMATION  UPDATE'
                mail = request.user.email
                try:
                    EmailThread(subject=email_subject, message=email_body, recipient_list=[mail]).start()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                except Exception as ex:
                    print(f"Error sending email: {ex}")
                    return HttpResponse('An error occurred while sending the email.')
                return redirect('home')
            
        return render(request, 'root/profile.html', {'form1': form1, 'form2': form2})
    
class ProfileView(View):
    def get(self,request):
        user_ip_address = request.META.get('REMOTE_ADDR')
        try:
            profile_obj = Profile.objects.get(owner=request.user)
        except:
            return redirect("login")
        profile = Profile.objects.get(owner=request.user)
        return render(request,'root/set-up-profile.html',{'profile':profile_obj,'user_ip_address': user_ip_address})




    

