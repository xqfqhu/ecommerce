from django import forms
from .models import UserBase, Address
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django_countries.fields import CountryField
from django.contrib.auth import password_validation


class RegistrationForm(forms.ModelForm):
    
    user_name = forms.CharField(
                                label = 'Enter Username',
                                min_length = 4,
                                max_length = 50,
                                help_text = 'Required',
                                )
    email = forms.EmailField(
                             max_length = 100,
                             help_text = 'required',
                             error_messages = {'required': 'Sorry, you will need an email'},
                            )
    password = forms.CharField(
                               label = 'Password',
                               widget = forms.PasswordInput,
                               )
    password2 = forms.CharField(
                               label = 'Pass validation',
                               widget = forms.PasswordInput,
                               # a widget is Djando's representation of an HTML input element
                               # the widget handles the rendering of the HTML and the extraction of data from a GET/POST dictionary that corresponds to the widget
                               # whenever you specify a field on a form, Django will use a default widget that is appropriate to the type of data that is to be displayed
                               # however, if you want to use a different widget for a field, you can use the widget argument on the field definition
                               )
    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)
    
    
    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name = user_name)
        if r.count():
            raise forms.ValidationError('Username already exists')
        return user_name
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = UserBase.objects.filter(email = email)
        if r.count():
            raise forms.ValidationError('Email already exists')
        return email
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeate Password'})

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(
        attrs = {'calss': 'form-control mb-3','placeholder': 'Username', 'id': 'login-username'}
    ))
    password = forms.CharField(widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))

class UserEditForm(forms.ModelForm):
    user_name = forms.CharField(
                                label = 'Username (cannot be changed)',
                                min_length = 4,
                                max_length = 50,
                                widget = forms.TextInput(
                                    attrs = {
                                        'class': 'form-control mb-3',
                                        'placeholder': 'Username',
                                        'id': 'form-username',
                                        'readonly':'readonly'
                                    }
                                )

                                )
    email = forms.EmailField(
                             label = 'Account Email (cannot be changed)',
                             max_length = 100,
                             widget = forms.TextInput(
                                    attrs = {
                                        'class': 'form-control mb-3',
                                        'placeholder': 'Email',
                                        'id': 'form-email',
                                        'readonly':'readonly'
                                    }
                                )
                            )
    
    class Meta:
        model = UserBase
        fields = ('email', 'user_name')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _key in self.fields:
            if _key == 'user_name' or _key == 'email':
                self.fields[_key].required = True
            else:
                self.fields[_key].required = False
        
        

class PwdResetForm(PasswordResetForm):
    email= forms.EmailField(
        label = 'Email',
        max_length = 254,
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control mb-3',
                'placeholder': 'Email',
                'id': 'form-email'
            }
        )
    )
    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email = email)
        if not u:
            raise forms.ValidationError('Unfortunately, we cannnot find that email address')
        else:
            return email
class pwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))
class AddressForm(forms.ModelForm):
    town_city = forms.CharField(
        max_length = 150,
        label = 'City or Town',
        ) 
    
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'postcode', 'address_line', 'address_line2', 'town_city', 'country', 'state']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address Line 1"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address Line 2"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Town/City"}
        )
        self.fields["state"].widget.attrs.update(
            {"class": "form-control mb-2 account-form",}
        )
        self.fields["country"].widget.attrs.update(
            {"class": "form-control mb-2 account-form",}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Postcode",}
        )
        for _key in self.fields:
            if _key in ['phone', 'address_line', 'town_city', 'country', ]:
                self.fields[_key].required = True
            else:
                self.fields[_key].required = False

