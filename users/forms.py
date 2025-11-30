from django.contrib.auth.models import  Group, Permission
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from events.forms import StyledFormMixin
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm


User = get_user_model()

class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        errors = []
        if len(password) != 8:
            errors.append('Passwrod must be  8 charecter long')
            
        if errors:
            raise forms.ValidationError(errors)
    
        return password
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists = User.objects.filter(email = email).exists()
        
        if is_exists:
            raise forms.ValidationError('Email already exist!! Please try different email address.')
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password do not match!!')  
        return cleaned_data      
        
class CustomUserUpdateForm(StyledFormMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        
    
    
        
class CustomLoginForm(StyledFormMixin, AuthenticationForm):
    
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)        
        
        
class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions =  forms.ModelMultipleChoiceField(
        queryset= Permission.objects.all(),
        widget= forms.CheckboxSelectMultiple,
        required= False,
        label= "Assign Permission"
    )       
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        
        
class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset = Group.objects.all(),
        label="Select a Role"
    )  
          
class GroupUpdateSelectForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset = Group.objects.all(),
        label="Select a Group"
    )        



class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'age', 'gender', 'phone' , 'blood_group', 'bio', 'profile_image', 'address', 'description']  


class PasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass

class PasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass


