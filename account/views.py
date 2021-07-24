
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import views as auth_views


from .forms import RegistrationForm, UserLoginForm, UserEditForm, PwdResetForm, pwdResetConfirmForm, AddressForm
from .models import UserBase, Address
from .token import account_activation_token
from order.views import user_orders
# Create your views here.

def account_register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        
        registerForm = RegistrationForm(data = request.POST)

        if registerForm.is_valid():
            user = registerForm.save(commit = False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # setup email
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            
            message = render_to_string('account/registration/account_activation_email.html', 
        
            {'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            # just transform user.pk to a format supported in url
            'token': account_activation_token.make_token(user)
            })
            
            user.email_user(subject=subject, message=message)
            
            
            return HttpResponse('registered successfully and activation sent')
        else:
            return render(request, 'account/registration/register.html', {'form': registerForm})
            # you'de have to tell django what to do is .is_valid() fails
            # recall that in resgitration.html, we have  {% if form.errors %} statement, which tells html what to print on form.errors
            # so if .is_valid() fails, we should render the unbounded form, as we do if we get a GET request
    else:
        registerForm = RegistrationForm()
        return render(request, 'account/registration/register.html', {'form': registerForm})

def account_activate(request, uidb64, token):
    try:
    
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = UserBase.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')

@login_required # this decorator asks django to check whether the user is loged in or not. allow user to access dashboad only if he/she is logged in
def dashboard(request):
    
    return render(request, 'account/user/dashboard.html')

def account_user_orders(request):
    orders = user_orders(request)
    return render(request, 'account/user/orders.html', {'orders': orders})
class customLogin(auth_views.LoginView):
    template_name = 'account/registration/login.html'
    form_class = UserLoginForm
class customLogout(auth_views.LogoutView):
    next_page = '/account/login'

@login_required
def edit_details(request):
    if request.method == 'GET':
        
        user_form = UserEditForm(instance = request.user)
    else:
        user_form = UserEditForm(instance = request.user, data = request.POST)
        if user_form.is_valid():
            user_form.save()
    return render(request, 'account/user/edit_details.html', {'user_form': user_form})

@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name = request.user.user_name)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

class customPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/user/password_reset_form.html'
    success_url = 'password_reset_email_confirm/'
    email_template_name = 'account/user/password_reset_email.html'
    form_class = PwdResetForm

class customPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/user/password_reset_confirm.html'
    success_url = 'passord_reset_complete/'
    form_class = pwdResetConfirmForm

def passwordResetEmailConfirm(request):
    
    return render(request, 'account/user/reset_status.html')
def passwordResetComplete(request):
    
    return render(request, 'account/user/reset_status.html')

@login_required
def add_address(request):
    if request.method == 'GET':
        address_form = AddressForm()
    else:
        address_form = AddressForm(data = request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit = False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse('account:addresses'))
    return render(request, 'account/user/add_address.html', {'form':address_form})
@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/user/addresses.html", {"addresses": addresses})


@login_required
def delete_address(request, address_id):
    
    address = get_object_or_404(Address, id = address_id)
    address.delete()
    addresses = Address.objects.filter(customer=request.user)
    address_qty = str(len(addresses))
    response = JsonResponse({'address_qty': address_qty})
    return response

@login_required
def edit_address(request, address_id):
    if request.method == 'GET':
        
        address = get_object_or_404(Address, id = address_id)
        address_form = AddressForm(instance = address)
        return render(request, 'account/user/edit_address.html', {'form': address_form, 'address':address})

        
    else:


        address = get_object_or_404(Address, id = address_id)
        address_form = AddressForm(instance = address, data = request.POST)
        return render(request, 'account/user/edit_address.html', {'form': address_form, 'address':address}) 

@login_required
def set_default(request, address_id):
    Address.objects.filter(customer = request.user, default = True).update(default = False)
    Address.objects.filter(customer = request.user, pk = address_id).update(default = True)
    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("payment:delivery_address")

    return redirect("account:addresses")