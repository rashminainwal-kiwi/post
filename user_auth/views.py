from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
import constants
from django.contrib.auth import authenticate 
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from .tokens import generate_tokens
from authentication.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode




def home(request):
    return render(request, 'index.html')


class register(View):
    """
    Creating a register class, and getting values
    Validating all fields with the  django default user methods
    Creating a user and saving the user
    Confirmation message goes to registered mail 
    user verify the mail 
    Returning and redirecting to templates for register form
    :param request: wsgi request

    """
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.method == 'POST':
            # Get form values
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            # Check if Passwords match
            if password == password2:  # matching
              # Check username
                if User.objects.filter(username=username).exists():
                    messages.error(
                        request, constants.ERROR['username']['already_taken'])
                    return redirect('register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(
                            request, constants.ERROR['email']['already_exists'])
                        return redirect('register')
                    else:
                        
                        user = User.objects.create_user(
                            username=username, password=password, email=email, first_name=first_name, last_name=last_name)

                        user.is_active = False
                        user.save()
                        messages.success(
                            request, constants.ERROR['register_succesfully']['registered'])

                        # Welcome Email
                        subject = "Welcome !!"
                        message = "Hello " + user.first_name + "!! \n" + \
                            "Welcome !! \n Thank you for visiting our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nRashmi"
                        from_email = EMAIL_HOST_USER
                        to_list = [user.email]
                        send_mail(subject, message, from_email,
                                  to_list, fail_silently=True)

                        # Email Address Confirmation Email
                        current_site = get_current_site(request)
                        email_subject = "Confirm your Email  for Login!!"
                        message2 = render_to_string('mail_conform.html', {

                            'name': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': generate_tokens.make_token(user),
                        })

                        email = EmailMessage(
                            email_subject,
                            message2,
                            EMAIL_HOST_USER,
                            [user.email],
                        )
                        email.fail_silently = True
                        email.send()
                        return redirect('login')
            else:
                messages.error(
                    request, constants.ERROR['password']['does_not_match'])
        return redirect('register')

class Activate(View):
    """
     Creating a activate class 
     decode the token using django decoder 
     if token match then user account is activated, return to login page
     else return activation failed
     :params request: wsgi request

    """
    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
         print(user)
        if user is not None:
             if token == token:
                user.is_active = True 
                user.save()
                messages.success(request, "Your Account has been activated!!")
                return redirect('login')
        else:
            return render(request, 'activation_failed.html')


# login class for login the user
class login(View):
    """
    Creating a login class
    authenticating with django user's authenticate method
    if user is authenticated , return to dashboard page
    give message for login success
    else give message for invalid credentials and redirect to login page
    :params request: wsgi request

    """

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                # messages.success(
                #     request, constants.ERROR['login_succesfully']['login'])
                return redirect('dashboard')

            else:
                messages.error(
                    request, constants.ERROR['credentials']['Invalid credentials'])
                return redirect('login')


class logout(View):
    """
    Creating a logout class
    after logout request, redirecting it to home
    :params request: wsgi request

    """
    def get(self, request):
        return redirect('login')

    def post(self, request):
        if request.method == 'POST':
            auth.logout(request)
            messages.Error(request, constants.ERROR['logout']['logout'])
        return redirect('home')


def dashboard(request):
    return render(request, 'dashboard.html')
